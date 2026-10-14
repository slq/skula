package pl.skula.android;

import org.json.JSONObject;
import java.text.Collator;
import java.util.*;

/** Pure presentation of the cached grade list; source JSON is never modified. */
final class GradeData {
    private GradeData() { }

    static String subject(JSONObject item) {
        return SchoolPresentation.gradeSubject(item.optString("subject"),
                item.optString("title"), item.optString("details"));
    }

    static List<JSONObject> sorted(List<JSONObject> items, int order) {
        List<JSONObject> result = new ArrayList<>(items);
        if (order == 3) {
            Collator polish = Collator.getInstance(Locale.forLanguageTag("pl"));
            result.sort((a, b) -> polish.compare(a.optString("title"), b.optString("title")));
        } else {
            Comparator<java.time.Instant> dates = Comparator.naturalOrder();
            if (order != 2) dates = dates.reversed();
            result.sort(Comparator.comparing(
                    item -> SchoolPresentation.gradeTime(item.optString("when")),
                    Comparator.nullsLast(dates)));
        }
        return result;
    }

    static final class Group {
        final String key, name;
        final List<JSONObject> items = new ArrayList<>();
        Group(String key, String name) { this.key = key; this.name = name; }
    }

    static List<Group> groups(List<JSONObject> sortedItems) {
        Map<String, Group> groups = new LinkedHashMap<>();
        for (JSONObject item : sortedItems) {
            String name = subject(item), key = name.toLowerCase(Locale.ROOT);
            groups.computeIfAbsent(key, unused -> new Group(key, name)).items.add(item);
        }
        List<Group> result = new ArrayList<>(groups.values());
        Collator polish = Collator.getInstance(Locale.forLanguageTag("pl"));
        result.sort((a, b) -> polish.compare(a.name, b.name));
        return result;
    }
}
