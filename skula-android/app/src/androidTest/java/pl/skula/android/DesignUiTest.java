package pl.skula.android;

import android.content.Intent;
import android.view.*;
import androidx.test.core.app.ActivityScenario;
import androidx.test.platform.app.InstrumentationRegistry;
import org.junit.Test;
import static org.junit.Assert.*;

/** The accepted design always exposes complete news and daily timetable lists. */
public class DesignUiTest {
    private int count(View view,String tag) {
        int total=tag.equals(view.getTag())?1:0;
        if(view instanceof ViewGroup)for(int i=0;i<((ViewGroup)view).getChildCount();i++)total+=count(((ViewGroup)view).getChildAt(i),tag);
        return total;
    }
    private void fullToday(MainActivity a) {
        View root=a.getWindow().getDecorView(),news=root.findViewWithTag("home_changes"),plan=root.findViewWithTag("home_plan");
        assertNotNull(news);assertNotNull(plan);
        assertEquals(7,count(news,"home_change"));
        assertNull(NavigationTestSupport.button(news,"Pokaż wszystkie zmiany"));
        assertEquals(4,count(plan,"home_lesson"));
        for(String title:new String[]{"Matematyka","Język polski","Język angielski","Biologia"})
            assertNotNull("Missing lesson: "+title,HomeworkCompletionTest.find(plan,title));
        assertNotNull(HomeworkCompletionTest.find(plan,"Koniec lekcji o 11:35"));
        assertNotNull(NavigationTestSupport.button(root,"Szukaj we wszystkich sekcjach"));
        assertNotNull(NavigationTestSupport.button(root,"Odśwież"));
        assertNotNull(NavigationTestSupport.button(root,"Konto"));
    }
    @Test public void allNewsAndEveryDailyLessonRemainExpandedAcrossNavigationAndRotation()throws Exception {
        HomeworkCompletionTest.blank();
        try(ActivityScenario<MainActivity> scenario=ActivityScenario.launch(new Intent(HomeworkCompletionTest.context(),MainActivity.class).putExtra("demo",true))) {
            HomeworkCompletionTest.ready(scenario);scenario.onActivity(this::fullToday);
            scenario.onActivity(a->NavigationTestSupport.button(a.getWindow().getDecorView(),"Jutro").performClick());
            InstrumentationRegistry.getInstrumentation().waitForIdleSync();
            scenario.onActivity(a->{
                View root=a.getWindow().getDecorView(),plan=root.findViewWithTag("home_plan");
                assertEquals(7,count(root.findViewWithTag("home_changes"),"home_change"));
                assertEquals(1,count(plan,"home_lesson"));
                assertNotNull(HomeworkCompletionTest.find(plan,"Historia"));
                NavigationTestSupport.button(root,"Dzisiaj").performClick();
                NavigationTestSupport.open(a,"Wiadomości");NavigationTestSupport.open(a,"Start");
            });
            scenario.recreate();HomeworkCompletionTest.ready(scenario);scenario.onActivity(this::fullToday);
        }
    }
    @Test public void unreadFilterAndCalendarLessonsPersistWithoutLosingOtherSources()throws Exception {
        HomeworkCompletionTest.blank();
        try(ActivityScenario<MainActivity> scenario=ActivityScenario.launch(new Intent(HomeworkCompletionTest.context(),MainActivity.class).putExtra("demo",true))) {
            HomeworkCompletionTest.ready(scenario);
            scenario.onActivity(a->{
                NavigationTestSupport.open(a,"Wiadomości");View root=a.getWindow().getDecorView();
                assertNotNull(HomeworkCompletionTest.find(root,"Materiały do powtórzenia"));
                NavigationTestSupport.button(root,"Nieprzeczytane · 2").performClick();
                assertNull(HomeworkCompletionTest.find(root,"Materiały do powtórzenia"));
                assertNotNull(HomeworkCompletionTest.find(root,"Zebranie rodziców w przyszłym tygodniu"));
            });
            scenario.recreate();
            scenario.onActivity(a->{
                View root=a.getWindow().getDecorView();
                assertTrue(NavigationTestSupport.button(root,"Nieprzeczytane · 2").isSelected());
                assertNull(HomeworkCompletionTest.find(root,"Materiały do powtórzenia"));
                NavigationTestSupport.button(root,"Wszystkie").performClick();
                assertNotNull(HomeworkCompletionTest.find(root,"Materiały do powtórzenia"));
                NavigationTestSupport.open(a,"Kalendarz");
                if(java.time.YearMonth.from(java.time.LocalDate.now().plusDays(1)).isAfter(java.time.YearMonth.now()))NavigationTestSupport.button(root,"›").performClick();
                assertNotNull(HomeworkCompletionTest.find(root,"Historia"));
                NavigationTestSupport.button(root,"Lista").performClick();
                ChangesFeedUiTest.described(root,"Źródło kalendarza: Plan lekcji").performClick();
                assertNull(HomeworkCompletionTest.find(root,"Historia"));
                assertNotNull(HomeworkCompletionTest.find(root,"Matematyka · sprawdzian"));
            });
            scenario.recreate();
            scenario.onActivity(a->{
                View root=a.getWindow().getDecorView();
                assertTrue(NavigationTestSupport.button(root,"Lista").isSelected());
                assertFalse(((android.widget.CheckBox)ChangesFeedUiTest.described(root,"Źródło kalendarza: Plan lekcji")).isChecked());
                assertNull(HomeworkCompletionTest.find(root,"Historia"));
                ChangesFeedUiTest.described(root,"Źródło kalendarza: Plan lekcji").performClick();
                assertNotNull(HomeworkCompletionTest.find(root,"Historia"));
                assertNotNull(HomeworkCompletionTest.find(root,"Matematyka · sprawdzian"));
            });
        }
    }
}
