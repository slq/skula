package pl.skula.android;

import java.time.LocalTime;
import java.time.format.DateTimeFormatter;
import java.util.regex.*;

/** Formats existing school text without inventing missing lesson times or marks. */
final class SchoolPresentation {
    private static final Pattern RANGE=Pattern.compile("^\\s*(\\d{1,2}:\\d{2})\\s*[–—-]\\s*(\\d{1,2}:\\d{2})\\s*(?:[·|]\\s*)?");
    private static final Pattern END=Pattern.compile("(?m)^Koniec:\\s*(\\d{1,2}:\\d{2})(?::\\d{2})?\\s*$");
    private static final Pattern GRADE=Pattern.compile("(?:\\s*·\\s*|:\\s*)([1-6][+-]?|np|nb|bz|[+-])$");
    private SchoolPresentation(){}
    static LocalTime parseTime(String value) {
        try{return LocalTime.parse(value,DateTimeFormatter.ofPattern("H:mm").withResolverStyle(java.time.format.ResolverStyle.STRICT));}catch(Exception ignored){return null;}
    }
    static LocalTime end(String subtitle,String details) {
        Matcher end=END.matcher(details);
        if(end.find())return parseTime(end.group(1));
        Matcher range=RANGE.matcher(subtitle);return range.find()?parseTime(range.group(2)):null;
    }
    static String lessonSubtitle(String subtitle) {
        Matcher range=RANGE.matcher(subtitle);
        return range.find()?subtitle.substring(range.end()).trim():subtitle;
    }
    static String grade(String title) {
        Matcher value=GRADE.matcher(title);return value.find()?value.group(1):"";
    }
    static String initials(String value) {
        String[] words=value.trim().split("\\s+");StringBuilder result=new StringBuilder();
        for(String word:words)if(!word.isEmpty()&&Character.isLetter(word.codePointAt(0))){
            result.appendCodePoint(Character.toUpperCase(word.codePointAt(0)));if(result.codePointCount(0,result.length())==2)break;
        }
        return result.length()==0?"—":result.toString();
    }
}
