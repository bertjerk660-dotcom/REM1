// New Vegas host HUD ownership only. This is NOT an original THUG2 UI renderer.
// Use the xNVSE SDK's menu lookup and trait setter; never ToggleMenus globally.
// The stored pointer is an identity token only, never dereferenced after a frame.
struct FalloutHudOwnership
{
    Tile* identity = nullptr;
    float previousVisibility = 1.0f;
    bool acquired = false;
};
static FalloutHudOwnership g_falloutHudOwnership;

static Tile* ResolveFalloutHudRoot()
{
    Menu* menu = InterfaceManager::GetMenuByType(kMenuType_HUDMain);
    return menu ? menu->tile : nullptr;
}

static void UpdateFalloutHudOwnership(bool skateActive)
{
    // Do not query the UI singleton during startup when nothing is owned.
    if (!skateActive && !g_falloutHudOwnership.acquired) return;
    Tile* current = ResolveFalloutHudRoot();
    if (!skateActive)
    {
        if (g_falloutHudOwnership.acquired && current &&
            current == g_falloutHudOwnership.identity)
        {
            CALL_MEMBER_FN(current, SetFloatValue)(
                Tile::kTileValue_visible,
                g_falloutHudOwnership.previousVisibility, true);
            _MESSAGE("[THUG2-HUD] restored FNV HUD visibility %.3f",
                g_falloutHudOwnership.previousVisibility);
        }
        g_falloutHudOwnership = FalloutHudOwnership{};
        return;
    }

    if (!current)
    {
        // A loading/menu rebuild can destroy the root. Do not retain stale ownership.
        g_falloutHudOwnership = FalloutHudOwnership{};
        return;
    }
    Tile::Value* visible = current->GetValue(Tile::kTileValue_visible);
    if (!visible || !std::isfinite(visible->num))
        return;
    if (!g_falloutHudOwnership.acquired ||
        current != g_falloutHudOwnership.identity)
    {
        g_falloutHudOwnership.identity = current;
        g_falloutHudOwnership.previousVisibility = visible->num;
        g_falloutHudOwnership.acquired = true;
        _MESSAGE("[THUG2-HUD] acquired FNV HUD root=%p previous visibility=%.3f",
            current, visible->num);
    }
    // The engine can recalculate HUD visibility. Reassert only while skate owns it.
    if (visible->num != 0.0f)
        CALL_MEMBER_FN(current, SetFloatValue)(Tile::kTileValue_visible, 0.0f, true);
}