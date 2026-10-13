package pl.skula.android;

import android.app.Dialog;
import android.content.ClipboardManager;
import android.content.Intent;
import android.graphics.Bitmap;
import android.view.View;
import android.view.WindowManager;
import android.view.inspector.WindowInspector;
import androidx.test.core.app.ActivityScenario;
import androidx.test.platform.app.InstrumentationRegistry;
import org.json.JSONArray;
import org.json.JSONObject;
import org.junit.Test;
import java.lang.reflect.Field;
import java.time.LocalDate;
import static org.junit.Assert.*;

/** Run only on the isolated emulator with synthetic data and no school account. */
public class CopyAndScreenshotUiTest {
    private static View dialogWith(String text) {
        for (View root : WindowInspector.getGlobalWindowViews())
            if (root.isShown() && NavigationTestSupport.button(root, "Zamknij") != null
                    && HomeworkCompletionTest.find(root, text) != null) return root;
        return null;
    }
    private static void assertScreenshotsAllowed(View root) {
        assertEquals(0, ((WindowManager.LayoutParams) root.getLayoutParams()).flags
                & WindowManager.LayoutParams.FLAG_SECURE);
    }
    private static String clipboard(MainActivity activity) {
        ClipboardManager clipboard = (ClipboardManager) activity.getSystemService(MainActivity.CLIPBOARD_SERVICE);
        assertNotNull(clipboard.getPrimaryClip());
        return clipboard.getPrimaryClip().getItemAt(0).getText().toString();
    }
    private static ActivityScenario<MainActivity> launch() throws Exception {
        HomeworkCompletionTest.blank();
        ActivityScenario<MainActivity> scenario = ActivityScenario.launch(
                new Intent(HomeworkCompletionTest.context(), MainActivity.class).putExtra("demo", true));
        HomeworkCompletionTest.ready(scenario);
        return scenario;
    }
    private static JSONObject item(String kind, String content) throws Exception {
        return new JSONObject().put("id", "synthetic-" + kind).put("title", "Żółć · " + kind)
                .put("when", "2026-10-13 10:30").put("details", content);
    }
    private static JSONObject offline(JSONObject sections) throws Exception {
        return new JSONObject().put("ready", true).put("mode", "offline")
                .put("year", HomeworkCompletionTest.year()).put("sections", sections);
    }

    @Test public void offlineScreenshotsWorkAndOnlyLoginWindowRemainsSecure() throws Exception {
        try (ActivityScenario<MainActivity> scenario = launch()) {
            JSONObject supplied = offline(new JSONObject());
            scenario.onActivity(a -> {
                a.onState(supplied);
                assertScreenshotsAllowed(a.getWindow().getDecorView());
                NavigationTestSupport.button(a.getWindow().getDecorView(), "Konto").performClick();
                try {
                    Field field = MainActivity.class.getDeclaredField("loginDialog");
                    field.setAccessible(true);
                    Dialog login = (Dialog) field.get(a);
                    assertNotNull(login);
                    assertNotEquals(0, login.getWindow().getAttributes().flags & WindowManager.LayoutParams.FLAG_SECURE);
                    login.dismiss();
                    assertScreenshotsAllowed(a.getWindow().getDecorView());
                } catch (ReflectiveOperationException error) { throw new AssertionError(error); }
            });
            InstrumentationRegistry.getInstrumentation().waitForIdleSync();
            Bitmap screenshot = InstrumentationRegistry.getInstrumentation().getUiAutomation().takeScreenshot();
            assertNotNull("System screenshot must be available outside login", screenshot);
            screenshot.recycle();
        }
    }

    @Test public void threeSectionsCopyExactTitleDateAndUntruncatedUnicodeBodyOffline() throws Exception {
        String content = "Pierwszy akapit: zażółć gęślą jaźń.\n\n" + "Długa treść. ".repeat(400);
        String[] kinds = {"announcements", "messages", "schedule"};
        String[] labels = {"Ogłoszenia", "Wiadomości", "Terminarz"};
        JSONObject sections = new JSONObject();
        for (String kind : kinds) sections.put(kind, new JSONArray().put(item(kind, content)));
        JSONObject supplied = offline(sections);
        try (ActivityScenario<MainActivity> scenario = launch()) {
            scenario.onActivity(a -> a.onState(supplied));
            for (int i = 0; i < kinds.length; i++) {
                final String title = "Żółć · " + kinds[i], label = labels[i];
                scenario.onActivity(a -> {
                    NavigationTestSupport.open(a, label);
                    View row = ChangesFeedUiTest.described(a.getWindow().getDecorView(), title + ". Otwórz szczegóły");
                    assertNotNull(row);
                    row.performClick();
                    View dialog = dialogWith(title);
                    assertNotNull(dialog);
                    assertScreenshotsAllowed(dialog);
                    NavigationTestSupport.button(dialog, "Kopiuj").performClick();
                    assertEquals(title + "\nData: 13.10.2026 · 10:30\n\n" + content, clipboard(a));
                    NavigationTestSupport.button(dialog, "Zamknij").performClick();
                });
            }
        }
    }

    @Test public void downloadedMessageKeepsDateAndCopiesFullBodyInsteadOfPreview() throws Exception {
        String title = "Zebranie rodziców w przyszłym tygodniu";
        String body = "Przykładowa treść wiadomości. Demo nie łączy się z kontem szkoły.";
        try (ActivityScenario<MainActivity> scenario = launch()) {
            scenario.onActivity(a -> {
                NavigationTestSupport.open(a, "Wiadomości");
                ChangesFeedUiTest.described(a.getWindow().getDecorView(), title + ". Otwórz szczegóły").performClick();
                NavigationTestSupport.button(dialogWith(title), "Pobierz treść").performClick();
            });
            long until = System.currentTimeMillis() + 15000;
            boolean[] ready = {false};
            while (System.currentTimeMillis() < until) {
                scenario.onActivity(a -> ready[0] = dialogWith(body) != null);
                if (ready[0]) break;
                Thread.sleep(50);
            }
            assertTrue("Full message did not open", ready[0]);
            scenario.onActivity(a -> {
                View dialog = dialogWith(body);
                assertScreenshotsAllowed(dialog);
                assertNull(NavigationTestSupport.button(dialog, "Pobierz treść"));
                NavigationTestSupport.button(dialog, "Kopiuj").performClick();
                assertEquals(title + "\nData: " + DisplayData.date(LocalDate.now() + " 09:20") + "\n\n" + body, clipboard(a));
                NavigationTestSupport.button(dialog, "Zamknij").performClick();
            });
        }
    }
}
