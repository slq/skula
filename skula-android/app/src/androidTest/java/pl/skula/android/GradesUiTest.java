package pl.skula.android;

import android.content.Intent;
import android.graphics.Bitmap;
import android.view.View;
import android.view.ViewGroup;
import android.view.accessibility.AccessibilityNodeInfo;
import android.widget.Button;
import android.widget.EditText;
import androidx.test.core.app.ActivityScenario;
import androidx.test.platform.app.InstrumentationRegistry;
import org.json.*;
import org.junit.Test;
import java.io.File;
import java.io.FileOutputStream;
import java.util.*;
import static org.junit.Assert.*;

/** Synthetic grades only, on the isolated emulator without a school account. */
public class GradesUiTest {
    private static JSONObject grade(String id, String title, String subject, String when, String details) throws Exception {
        return new JSONObject().put("id",id).put("kind","grades").put("title",title)
                .put("subject",subject).put("when",when).put("subtitle","Przykładowa ocena")
                .put("details",details);
    }
    private static List<JSONObject> grades() throws Exception {
        return Arrays.asList(
                grade("math-old","Matematyka: 4","matematyka","2026-10-11","Sprawdzian: ułamki"),
                grade("english","Język angielski: 5","Język angielski","2026-10-13","Odpowiedź ustna"),
                grade("math-new","Matematyka: 5+","Matematyka","2026-10-14","Przykładowy komentarz matematyka"),
                grade("art","Plastyka — ocena opisowa","","2026-10-10","Przedmiot: Plastyka\nOpis: Staranna praca."));
    }
    private static JSONObject cache() throws Exception {
        return new JSONObject().put("ready",true).put("mode","demo").put("status","Dane demonstracyjne")
                .put("sections",new JSONObject().put("grades",new JSONArray(grades())))
                .put("updated_at",new JSONObject().put("grades","2026-10-14T12:00:00"))
                .put("errors",new JSONObject());
    }
    private static View root(MainActivity a) { return a.getWindow().getDecorView(); }
    private static Button mode(MainActivity a,String name) { return NavigationTestSupport.button(root(a),name); }
    private static Button header(MainActivity a,String key) { return root(a).findViewWithTag("grade_header:"+key); }
    private static EditText search(MainActivity a) { return (EditText)ChangesFeedUiTest.described(root(a),"Wyszukiwanie w bieżącej sekcji"); }
    private static List<String> rowIds(View view) {
        List<String> result=new ArrayList<>();
        String tag=String.valueOf(view.getTag());
        if(tag.startsWith("grade_item:"))result.add(tag.substring("grade_item:".length()));
        if(view instanceof ViewGroup)for(int i=0;i<((ViewGroup)view).getChildCount();i++)result.addAll(rowIds(((ViewGroup)view).getChildAt(i)));
        return result;
    }
    private static ActivityScenario<MainActivity> launch() throws Exception {
        HomeworkCompletionTest.blank();
        ActivityScenario<MainActivity> scenario=ActivityScenario.launch(new Intent(HomeworkCompletionTest.context(),MainActivity.class).putExtra("demo",true));
        HomeworkCompletionTest.ready(scenario);
        return scenario;
    }
    private static void open(ActivityScenario<MainActivity> scenario,JSONObject cache) {
        scenario.onActivity(a->{a.onState(cache);NavigationTestSupport.open(a,"Oceny");});
        InstrumentationRegistry.getInstrumentation().waitForIdleSync();
    }
    private static void screenshot(String name) throws Exception {
        if(!InstrumentationRegistry.getArguments().getString("grades_screenshots","false").equals("true"))return;
        InstrumentationRegistry.getInstrumentation().waitForIdleSync();
        Bitmap image=InstrumentationRegistry.getInstrumentation().getUiAutomation().takeScreenshot();
        assertNotNull(image);
        try(FileOutputStream out=new FileOutputStream(new File(HomeworkCompletionTest.context().getExternalFilesDir(null),name+".png"))) {
            assertTrue(image.compress(Bitmap.CompressFormat.PNG,100,out));
        }finally{image.recycle();}
    }

    @Test public void groupingAndDateOrderPreserveLegacyDescriptiveAndUndatedGrades()throws Exception {
        List<JSONObject> rows=new ArrayList<>(grades());
        rows.add(grade("undated","Matematyka: +","Matematyka","","Aktywność"));
        String original=new JSONArray(rows).toString();
        List<JSONObject> ordered=GradeData.sorted(rows,0);
        assertEquals("math-new",ordered.get(0).getString("id"));
        assertEquals("undated",ordered.get(4).getString("id"));
        List<GradeData.Group> grouped=GradeData.groups(ordered);
        assertEquals(3,grouped.size());
        assertEquals("Język angielski",grouped.get(0).name);
        assertEquals("matematyka",grouped.get(1).key);
        assertEquals(3,grouped.get(1).items.size());
        assertEquals("math-new",grouped.get(1).items.get(0).getString("id"));
        assertEquals("Plastyka",grouped.get(2).name);
        assertEquals("art",grouped.get(2).items.get(0).getString("id"));
        assertEquals("art",GradeData.sorted(rows,2).get(0).getString("id"));
        assertEquals("undated",GradeData.sorted(rows,2).get(4).getString("id"));
        assertEquals(original,new JSONArray(rows).toString());
    }

    @Test public void modesKeepAllGradesAndOpenTheExactCachedDetail()throws Exception {
        JSONObject cache=cache();
        try(ActivityScenario<MainActivity> scenario=launch()) {
            open(scenario,cache);
            scenario.onActivity(a->{
                assertTrue(mode(a,"Według daty").isSelected());
                assertEquals(Arrays.asList("math-new","english","math-old","art"),rowIds(root(a)));
            });
            screenshot("grades-date");
            scenario.onActivity(a->{
                mode(a,"Według przedmiotów").performClick();
                assertTrue(mode(a,"Według przedmiotów").isSelected());
                assertEquals(Arrays.asList("english","math-new","math-old","art"),rowIds(root(a)));
                assertNotNull(HomeworkCompletionTest.find(root(a),"Ocen: 4 · Przedmiotów: 3"));
                assertTrue(header(a,"matematyka").getContentDescription().toString().contains("Liczba ocen: 2"));
            });
            screenshot("grades-subjects");
            scenario.onActivity(a->root(a).findViewWithTag("grade_item:math-new").performClick());
            InstrumentationRegistry.getInstrumentation().waitForIdleSync();
            // The accessibility window can lag behind the UI thread while the dialog animates.
            AccessibilityNodeInfo dialog=null;
            long deadline=android.os.SystemClock.uptimeMillis()+5000;
            while(android.os.SystemClock.uptimeMillis()<deadline) {
                AccessibilityNodeInfo candidate=InstrumentationRegistry.getInstrumentation().getUiAutomation().getRootInActiveWindow();
                if(candidate!=null&&!candidate.findAccessibilityNodeInfosByText("Przykładowy komentarz matematyka").isEmpty()) {
                    dialog=candidate;
                    break;
                }
                Thread.sleep(30);
            }
            assertNotNull("Grade details did not appear in the accessibility window",dialog);
            for(AccessibilityNodeInfo node:dialog.findAccessibilityNodeInfosByText("Zamknij"))
                if(node.isClickable())node.performAction(AccessibilityNodeInfo.ACTION_CLICK);
            scenario.onActivity(a->{mode(a,"Według daty").performClick();assertEquals(Arrays.asList("math-new","english","math-old","art"),rowIds(root(a)));});
        }
    }

    @Test public void searchAndOfflineErrorsDoNotDropOrModifyCachedGrades()throws Exception {
        JSONObject cache=cache();
        cache.put("mode","offline");
        cache.getJSONObject("errors").put("grades","Przykładowy błąd odczytu");
        String original=cache.toString();
        try(ActivityScenario<MainActivity> scenario=launch()) {
            open(scenario,cache);
            scenario.onActivity(a->{
                mode(a,"Według przedmiotów").performClick();
                assertNotNull(HomeworkCompletionTest.find(root(a),"Przykładowy błąd odczytu"));
            });
            scenario.onActivity(a->{
                search(a).setText("Sprawdzian");
                assertEquals(Collections.singletonList("math-old"),rowIds(root(a)));
                assertNull(header(a,"język angielski"));
                assertTrue(header(a,"matematyka").getContentDescription().toString().contains("Liczba ocen: 1"));
                search(a).setText("Brak pasujących ocen");
                assertTrue(rowIds(root(a)).isEmpty());
                assertNotNull(HomeworkCompletionTest.find(root(a),"Brak wyników. Zmień lub wyczyść wyszukiwanie."));
                search(a).setText("");
                assertEquals(4,rowIds(root(a)).size());
                assertNotNull(HomeworkCompletionTest.find(root(a),"Przykładowy błąd odczytu"));
            });
            assertEquals(original,cache.toString());
        }
    }

    @Test public void groupingCollapsedSubjectsAndQuerySurviveNavigationAndRecreation()throws Exception {
        JSONObject cache=cache();
        try(ActivityScenario<MainActivity> scenario=launch()) {
            open(scenario,cache);
            scenario.onActivity(a->{
                mode(a,"Według przedmiotów").performClick();
                header(a,"matematyka").performClick();
                assertEquals(Arrays.asList("english","art"),rowIds(root(a)));
                a.onState(cache);
                assertEquals(Arrays.asList("english","art"),rowIds(root(a)));
                NavigationTestSupport.open(a,"Wiadomości");
                NavigationTestSupport.open(a,"Oceny");
                assertEquals(Arrays.asList("english","art"),rowIds(root(a)));
            });
            scenario.recreate();
            InstrumentationRegistry.getInstrumentation().waitForIdleSync();
            scenario.onActivity(a->{
                a.onState(cache);
                assertTrue(mode(a,"Według przedmiotów").isSelected());
                assertEquals(Arrays.asList("english","art"),rowIds(root(a)));
                header(a,"matematyka").performClick();
                assertEquals(4,rowIds(root(a)).size());
                search(a).setText("matematyka");
            });
            scenario.recreate();
            InstrumentationRegistry.getInstrumentation().waitForIdleSync();
            scenario.onActivity(a->{
                a.onState(cache);
                assertTrue(mode(a,"Według przedmiotów").isSelected());
                assertEquals("matematyka",search(a).getText().toString());
                assertEquals(Arrays.asList("math-new","math-old"),rowIds(root(a)));
            });
        }
    }
}
