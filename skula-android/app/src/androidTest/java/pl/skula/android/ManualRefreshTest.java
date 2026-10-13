package pl.skula.android;

import android.content.*;
import android.os.Build;
import androidx.test.core.app.ActivityScenario;
import androidx.test.platform.app.InstrumentationRegistry;
import com.chaquo.python.*;
import com.chaquo.python.android.AndroidPlatform;
import org.json.JSONObject;
import org.junit.Test;
import static org.junit.Assert.*;

/** Real refresh button and repository; synthetic responses on a blank emulator. */
public class ManualRefreshTest {
    private void idle(MobileRepository repo) throws Exception {
        java.lang.reflect.Field busy = MobileRepository.class.getDeclaredField("busy"); busy.setAccessible(true);
        java.lang.reflect.Field ready = MobileRepository.class.getDeclaredField("initialized"); ready.setAccessible(true);
        long deadline = System.currentTimeMillis() + 20000;
        while ((!ready.getBoolean(repo) || busy.getBoolean(repo)) && System.currentTimeMillis() < deadline) Thread.sleep(30);
        assertTrue(ready.getBoolean(repo)); assertFalse("Refresh timed out", busy.getBoolean(repo));
        InstrumentationRegistry.getInstrumentation().waitForIdleSync();
    }
    private int reads(Python py, PyObject scope) {
        return py.getModule("builtins").callAttr("eval", "SyntheticConnector.reads", scope).toInt();
    }
    @Test public void manualReadsBypassCooldownButAutomaticAndServerLimitsRemain() throws Exception {
        assertTrue("Use a blank emulator", Build.HARDWARE.equals("ranchu") || Build.HARDWARE.equals("goldfish"));
        Context c = InstrumentationRegistry.getInstrumentation().getTargetContext();
        SecureStore store = new SecureStore(c); String original = store.read();
        assertTrue("Never run with a school account", original.isEmpty() || new JSONObject(original).isNull("credentials"));
        if (!Python.isStarted()) Python.start(new AndroidPlatform(c));
        Python py = Python.getInstance(); PyObject scope = py.getModule("builtins").callAttr("dict");
        py.getModule("builtins").callAttr("exec", """
            import mobile_bridge as m
            from datetime import date
            _original_service = m._service
            class SyntheticConnector:
                reads = 0
                rate_limited = False
                def __init__(self, *args): pass
                def connect(self): pass
                def close(self): pass
                def fetch(self, kind):
                    SyntheticConnector.reads += 1
                    if SyntheticConnector.rate_limited:
                        raise m.ConnectorError('Synthetic rate limit', rate_limited=True)
                    return [{'id': kind + ':synthetic-refresh', 'kind': kind, 'title': 'SYNTHETIC_REFRESH',
                             'subtitle': '', 'details': '', 'when': date.today().isoformat(), 'unread': False, 'url': ''}]
            m._service = m.MobileService(SyntheticConnector)
            """, scope);
        PyObject service = py.getModule("mobile_bridge").callAttr("get_service");
        service.callAttr("connect", "synthetic-refresh-profile", "test-only-password", true, false);
        store.write(service.callAttr("export_json").toString());
        java.lang.reflect.Field elapsed = SyncPolicy.class.getDeclaredField("lastElapsed"); elapsed.setAccessible(true);
        elapsed.setLong(null, -1); c.getSharedPreferences("sync_clock", 0).edit().clear().commit();
        MobileRepository repo = MobileRepository.get(c); boolean background = BackgroundSync.enabled(c), night = BackgroundSync.nightEnabled(c);
        try {
            BackgroundSync.nightEnabled(c, false);
            BackgroundSync.enabled(c, false);
            InstrumentationRegistry.getInstrumentation().runOnMainSync(() -> { repo.focused(true); repo.open(); }); idle(repo);
            assertEquals(7, reads(py, scope)); assertTrue(SyncPolicy.remaining(c) > 0);
            InstrumentationRegistry.getInstrumentation().runOnMainSync(repo::open); idle(repo);
            assertEquals("Automatic foreground read must wait", 7, reads(py, scope));
            try (ActivityScenario<MainActivity> scenario = ActivityScenario.launch(new Intent(c, MainActivity.class))) {
                InstrumentationRegistry.getInstrumentation().waitForIdleSync();
                scenario.onActivity(a -> {
                    android.widget.Button button = NavigationTestSupport.button(a.getWindow().getDecorView(), "Odśwież");
                    assertNotNull(button); assertTrue(button.isEnabled()); assertTrue(button.performClick());
                    assertFalse("Refresh stays disabled while fetching", button.isEnabled());
                    repo.refresh(); // Busy requests must not queue an additional read.
                }); idle(repo);
                assertEquals("Manual refresh must fetch during cooldown", 14, reads(py, scope));
                scenario.onActivity(a -> assertTrue(NavigationTestSupport.button(a.getWindow().getDecorView(), "Odśwież").performClick())); idle(repo);
                assertEquals("Repeated manual refresh must fetch", 21, reads(py, scope));
                assertTrue("Manual refresh delays automatic reads", SyncPolicy.remaining(c) > 0);
                InstrumentationRegistry.getInstrumentation().runOnMainSync(repo::open); idle(repo); assertEquals(21, reads(py, scope));
                BackgroundSync.enabled(c, true);
                java.util.concurrent.CountDownLatch done = new java.util.concurrent.CountDownLatch(1);
                InstrumentationRegistry.getInstrumentation().runOnMainSync(() -> repo.backgroundRefresh(done::countDown));
                assertTrue(done.await(20, java.util.concurrent.TimeUnit.SECONDS));
                assertEquals("Background reads must also wait after manual refresh", 21, reads(py, scope));
                BackgroundSync.enabled(c, false);
                py.getModule("builtins").callAttr("exec", "SyntheticConnector.rate_limited = True", scope);
                InstrumentationRegistry.getInstrumentation().runOnMainSync(repo::refresh); idle(repo); assertEquals(22, reads(py, scope));
                InstrumentationRegistry.getInstrumentation().runOnMainSync(repo::refresh); idle(repo);
                assertEquals("Manual refresh preserves the server rate limit", 22, reads(py, scope));
            }
        } finally {
            BackgroundSync.nightEnabled(c, night); BackgroundSync.enabled(c, background);
            if (original.isEmpty()) store.clear(); else store.write(original);
            py.getModule("builtins").callAttr("exec", "m._service = _original_service", scope);
            elapsed.setLong(null, -1); c.getSharedPreferences("sync_clock", 0).edit().clear().commit();
        }
    }
}
