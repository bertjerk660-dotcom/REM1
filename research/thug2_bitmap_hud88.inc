// Original THUG2 glyph atlas rendering; this is a host renderer, not a QB VM.
struct THUGGlyph88 { unsigned short x,y,w,h,baseline; bool present; };
#include "thug2_font_metrics88.inc"
static Gdiplus::Image* g_thugTitleFont88 = nullptr;
static Gdiplus::Image* g_thugTrickFont88 = nullptr;
static DWORD g_thugFontRetry88 = 0;
static bool EnsureTHUGFonts88()
{
    if (g_thugTitleFont88 && g_thugTrickFont88) return true;
    DWORD now = GetTickCount();
    if (g_thugFontRetry88 && now - g_thugFontRetry88 < 5000) return false;
    g_thugFontRetry88 = now;
    if (!g_thugTitleFont88) g_thugTitleFont88 = LoadOverlayImage(L"thug2\\fonts\\testtitle.png");
    if (!g_thugTrickFont88) g_thugTrickFont88 = LoadOverlayImage(L"thug2\\fonts\\newtrickfont.png");
    return g_thugTitleFont88 && g_thugTrickFont88;
}
static void DrawTHUGText88(Gdiplus::Graphics& g, const char* text,
    bool trick, float x, float y, float scale, bool centered)
{
    if (!text || !EnsureTHUGFonts88()) return;
    const THUGGlyph88* glyphs = trick ? kTHUGTrickGlyphs88 : kTHUGTitleGlyphs88;
    Gdiplus::Image* atlas = trick ? g_thugTrickFont88 : g_thugTitleFont88;
    float baseline = trick ? kTHUGTrickBaseline88 : kTHUGTitleBaseline88;
    float spacing = trick ? 10.0f : 12.0f; // startup.qb.q space_spacing; char_spacing=0
    float width = 0;
    for (const unsigned char* p = reinterpret_cast<const unsigned char*>(text); *p; ++p)
        width += (*p == ' ' ? spacing : glyphs[*p].w) * scale;
    if (centered) x -= width * 0.5f;
    for (const unsigned char* p = reinterpret_cast<const unsigned char*>(text); *p; ++p)
    {
        if (*p == ' ') { x += spacing*scale; continue; }
        const THUGGlyph88& c = glyphs[*p];
        if (c.present && c.w && c.h)
        {
            Gdiplus::RectF dst(x, y+(baseline-c.baseline)*scale, c.w*scale,c.h*scale);
            g.DrawImage(atlas,dst,c.x,c.y,c.w,c.h,Gdiplus::UnitPixel);
        }
        x += c.w*scale;
    }
}
// Partial source-layout adapter. Original sprites/fonts, no invented font fallback.
// Score/state still comes from the existing bridge, not original THUG2 scoring.
static void PaintTHUGHud88(HWND hwnd, HDC dc)
{
    RECT r={}; GetClientRect(hwnd,&r);
    HBRUSH key=CreateSolidBrush(RGB(1,2,3)); FillRect(dc,&r,key); DeleteObject(key);
    if (!g_skate.active || r.right<=0 || r.bottom<=0) return;
    EnsureOverlayImages();
    Gdiplus::Graphics g(dc);
    const float sx=r.right/640.0f, sy=r.bottom/448.0f;
    const float scale=sx<sy?sx:sy;
    g.TranslateTransform((r.right-640.0f*scale)*0.5f,0);
    g.ScaleTransform(scale,scale);
    // panelstuff.qb.q: the_score=(136,15), child score sprite=(-17,23).
    static Gdiplus::Image* backing=nullptr;
    if (!backing) backing=LoadOverlayImage(L"thug2\\score_small.png");
    if (backing) g.DrawImage(backing,Gdiplus::RectF(119,38,
        backing->GetWidth()*1.2f,backing->GetHeight()*0.85f));
    // Inherited score-sprite scale applied to local position/scale.
    if (g_thugSpecialBar)
    {
        float fill = std::isfinite(g_skate.special01) ? g_skate.special01 : 0;
        if(fill<0)fill=0; if(fill>1)fill=1;
        if(fill>0) g.DrawImage(g_thugSpecialBar,
            Gdiplus::RectF(129.8f,68.6f,g_thugSpecialBar->GetWidth()*1.2f*fill,
            g_thugSpecialBar->GetHeight()*0.85f*1.1f),
            0,0,g_thugSpecialBar->GetWidth()*fill,
            static_cast<float>(g_thugSpecialBar->GetHeight()),Gdiplus::UnitPixel);
    }
    if(g_thugSpecial) g.DrawImage(g_thugSpecial,Gdiplus::RectF(131,66.9f,
        g_thugSpecial->GetWidth()*1.2f*1.73f,g_thugSpecial->GetHeight()*0.85f*0.87f));
    char score[80]={};
    std::snprintf(score,sizeof(score),"%.0f",g_skate.totalScore);
    DrawTHUGText88(g,score,false,136,15,1,false);
    if(g_skate.comboActive)
    {
        std::snprintf(score,sizeof(score),"%.0f X %.0f",g_skate.comboScore,g_skate.comboMultiplier);
        // Temporary combo container position: full script morph/timing port remains pending.
        DrawTHUGText88(g,score,false,320,365,1,true);
        DrawTHUGText88(g,g_skate.lastTrick,true,320,393,0.7f,true);
    }
    if(g_skate.moveState==SkateMoveState::Grind || g_skate.moveState==SkateMoveState::Manual ||
       g_skate.moveState==SkateMoveState::Lip || g_skate.moveState==SkateMoveState::Skitch)
    {
        // panelstuff balance_meter_info: first normal-screen meter position.
        const float x=320,y=165;
        if(g_thugBalanceMeter) g.DrawImage(g_thugBalanceMeter,
            Gdiplus::RectF(x-g_thugBalanceMeter->GetWidth()*0.5f,
            y-g_thugBalanceMeter->GetHeight()*0.5f,
            static_cast<float>(g_thugBalanceMeter->GetWidth()),
            static_cast<float>(g_thugBalanceMeter->GetHeight())));
        // Original seven-point arrow curve, interpolated; input state is bridge-provided.
        const float xx[7]={0,10,20,30,40,50,60}, yy[7]={-17,-17,-15,-11,-6,1,12};
        float b=std::isfinite(g_skate.balance)?g_skate.balance:0;
        if(b<-1)b=-1; if(b>1)b=1;
        float t=std::fabs(b)*6; int i=static_cast<int>(t); if(i>5)i=5;
        float f=t-i, ax=(xx[i]+(xx[i+1]-xx[i])*f)*(b<0?-1:1), ay=yy[i]+(yy[i+1]-yy[i])*f;
        if(g_thugBalanceArrow) g.DrawImage(g_thugBalanceArrow,
            Gdiplus::RectF(x+ax-g_thugBalanceArrow->GetWidth()*0.5f,
            y+ay-g_thugBalanceArrow->GetHeight()*0.5f,
            static_cast<float>(g_thugBalanceArrow->GetWidth()),
            static_cast<float>(g_thugBalanceArrow->GetHeight())));
    }
}
