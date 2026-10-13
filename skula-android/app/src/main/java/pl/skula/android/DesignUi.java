package pl.skula.android;

import android.content.Context;
import android.content.res.ColorStateList;
import android.graphics.*;
import android.graphics.drawable.*;
import android.view.*;
import android.widget.*;

/** Shared visual tokens and native, accessible controls for the selected Skula design. */
final class DesignUi {
    static final int BG=0xfff4f7f7, INK=0xff17354a, MUTED=0xff687b84, TEAL=0xff087c75;
    static final int DARK=0xff153d46, LINE=0xffe0e9e7, MINT=0xffe3f1ed, WHITE=Color.WHITE;
    private DesignUi() {}
    static int dp(Context context,int value){return Math.round(value*context.getResources().getDisplayMetrics().density);}
    static GradientDrawable surface(Context c,int color,int radius,boolean border) {
        GradientDrawable drawable=new GradientDrawable();drawable.setColor(color);drawable.setCornerRadius(dp(c,radius));
        if(border)drawable.setStroke(dp(c,1),LINE);
        return drawable;
    }
    static android.graphics.drawable.Drawable ripple(Context c,int color,int radius,boolean border) {
        return new RippleDrawable(ColorStateList.valueOf(0x20087c75),surface(c,color,radius,border),surface(c,WHITE,radius,false));
    }
    static void clickable(View view,int color,int radius,Runnable action) {
        view.setBackground(ripple(view.getContext(),color,radius,false));
        view.setFocusable(true);view.setOnClickListener(v->action.run());
    }
    static void quiet(Button b,boolean selected) {
        b.setTextColor(new ColorStateList(new int[][]{{-android.R.attr.state_enabled},{}},new int[]{0xff8a9b9f,selected?TEAL:MUTED}));
        b.setBackground(ripple(b.getContext(),selected?MINT:Color.TRANSPARENT,10,false));
        b.setSelected(selected);
    }
    static Button iconButton(Context c,int resource,String label,Runnable action) {
        Button button=ButtonStyles.make(c,"",action,false);button.setContentDescription(label);button.setTooltipText(label);
        button.setPadding(dp(c,12),dp(c,12),dp(c,12),dp(c,12));
        android.graphics.drawable.Drawable icon=c.getDrawable(resource).mutate();icon.setTint(INK);icon.setBounds(0,0,dp(c,24),dp(c,24));
        button.setCompoundDrawables(icon,null,null,null);button.setBackground(ripple(c,Color.TRANSPARENT,24,false));
        button.setLayoutParams(new LinearLayout.LayoutParams(dp(c,48),dp(c,48)));
        return button;
    }
    static ImageView icon(Context c,int resource,int tint) {
        ImageView icon=new ImageView(c);icon.setImageResource(resource);icon.setImageTintList(ColorStateList.valueOf(tint));
        icon.setImportantForAccessibility(View.IMPORTANT_FOR_ACCESSIBILITY_NO);
        return icon;
    }
    static void navigation(Button button,boolean selected) {
        button.setTextColor(selected?TEAL:MUTED);button.setSelected(selected);
        Context c=button.getContext();
        button.setBackground(new RippleDrawable(ColorStateList.valueOf(0x18087c75),new NavigationPill(c,selected),surface(c,WHITE,12,false)));
        for(android.graphics.drawable.Drawable icon:button.getCompoundDrawables())if(icon!=null)icon.setTint(selected?TEAL:MUTED);
    }
    private static final class NavigationPill extends android.graphics.drawable.Drawable {
        private final Paint paint=new Paint(Paint.ANTI_ALIAS_FLAG);private final Context context;private final boolean selected;
        NavigationPill(Context c,boolean selected){context=c;this.selected=selected;paint.setColor(MINT);}
        @Override public void draw(Canvas canvas){
            if(!selected)return;Rect b=getBounds();float width=Math.min(b.width()-dp(context,6),dp(context,54));
            float left=b.exactCenterX()-width/2;
            canvas.drawRoundRect(left,b.top+dp(context,3),left+width,b.top+dp(context,34),dp(context,12),dp(context,12),paint);
        }
        @Override public void setAlpha(int alpha){paint.setAlpha(alpha);}
        @Override public void setColorFilter(ColorFilter filter){paint.setColorFilter(filter);}
        @Override public int getOpacity(){return PixelFormat.TRANSLUCENT;}
    }
}
