package pl.skula.android;

import java.time.LocalTime;
import org.junit.Test;
import static org.junit.Assert.*;

public class SchoolPresentationTest {
    @Test public void lessonEndUsesExplicitTimesAndNeverInventsDuration() {
        assertEquals(LocalTime.of(8,45),SchoolPresentation.end("08:00–08:45 · sala 12",""));
        assertEquals(LocalTime.of(9,40),SchoolPresentation.end("Lekcja 2 · Jan Nowak, sala 6","Początek: 08:55\nKoniec: 09:40"));
        assertEquals(LocalTime.of(10,35),SchoolPresentation.end("09:50 - 10:30 | sala 18","Koniec: 10:35:00"));
        assertNull(SchoolPresentation.end("Lekcja 1 · sala 12","Początek: 08:00"));
        assertNull(SchoolPresentation.end("08:00–99:00 · sala 12",""));
        assertNull(SchoolPresentation.parseTime("24:00"));
        assertNull(SchoolPresentation.parseTime("9:75"));
    }
    @Test public void lessonMetadataPreservesTeacherRoomAndUnrecognizedFormats() {
        assertEquals("sala 12",SchoolPresentation.lessonSubtitle("08:00–08:45 · sala 12"));
        assertEquals("Jan Nowak · sala 7",SchoolPresentation.lessonSubtitle("8:00 - 8:45 | Jan Nowak · sala 7"));
        assertEquals("Lekcja 1 · Jan Nowak, sala 12",SchoolPresentation.lessonSubtitle("Lekcja 1 · Jan Nowak, sala 12"));
        assertEquals("Od 8 do 9 · sala 1",SchoolPresentation.lessonSubtitle("Od 8 do 9 · sala 1"));
    }
    @Test public void marksDoNotTurnDescriptiveGradesIntoInventedNumbers() {
        assertEquals("5+",SchoolPresentation.grade("Matematyka · 5+"));
        assertEquals("4-",SchoolPresentation.grade("Polski: 4-"));
        assertEquals("np",SchoolPresentation.grade("Biologia · np"));
        assertEquals("",SchoolPresentation.grade("Praca domowa bardzo dobra"));
        assertEquals("",SchoolPresentation.grade("Historia · 15"));
    }
    @Test public void senderInitialsSupportPolishNamesAndWhitespace() {
        assertEquals("ŁŻ",SchoolPresentation.initials("  Łukasz \t Żak "));
        assertEquals("AN",SchoolPresentation.initials("Anna Nowak Kowalska"));
        assertEquals("—",SchoolPresentation.initials("123"));
        assertEquals("—",SchoolPresentation.initials(""));
    }


    @Test public void gradeSubjectsSupportMetadataAndOlderCachedFormats() {
        assertEquals("Matematyka",SchoolPresentation.gradeSubject(" Matematyka ","5",""));
        assertEquals("Wiedza o społeczeństwie",SchoolPresentation.gradeSubject("","5","Ocena: 5\nPrzedmiot: Wiedza o społeczeństwie\nSemestr: 1"));
        assertEquals("Edukacja: bezpieczeństwo",SchoolPresentation.gradeSubject("","Edukacja: bezpieczeństwo: 4+",""));
        assertEquals("Plastyka",SchoolPresentation.gradeSubject("","Plastyka — ocena opisowa",""));
        assertEquals("Język angielski",SchoolPresentation.gradeSubject("","Język angielski · 5",""));
        assertEquals("Bez przedmiotu",SchoolPresentation.gradeSubject(null,null,null));
    }
    @Test public void gradeDatesUseActualInstantsAndLeaveUnknownDatesUnsorted() {
        assertEquals(java.time.Instant.parse("2026-10-14T08:00:00Z"),SchoolPresentation.gradeTime("2026-10-14T10:00:00+02:00"));
        assertNotNull(SchoolPresentation.gradeTime("2026-10-14 10:00:00"));
        assertNotNull(SchoolPresentation.gradeTime("2026-10-14"));
        assertNull(SchoolPresentation.gradeTime("brak daty"));
        assertNull(SchoolPresentation.gradeTime(""));
    }
}
