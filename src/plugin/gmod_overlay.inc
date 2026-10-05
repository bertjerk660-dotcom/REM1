
static HWND g_gmodSpawnWindow = nullptr;
static HWND g_physBeamWindow = nullptr;
static HWND g_thugHudWindow = nullptr;
static HWND g_falloutGameWindow = nullptr;
static bool g_overlayClassesRegistered = false;
static int g_spawnHoveredItem = -1;
static int g_spawnCategoryScroll = 0;
static int g_spawnHoveredTool = -1;
static constexpr int kToolDuplicatorIndex = 7;
static constexpr int kToolRemoverIndex = 29;
static constexpr int kSpawnCategoryListTop = 158;

static Gdiplus::Image* g_uiContentNormal = nullptr;
static Gdiplus::Image* g_uiContentHover = nullptr;
static Gdiplus::Image* g_uiNpc = nullptr;
static Gdiplus::Image* g_uiTool = nullptr;
static Gdiplus::Image* g_uiGun = nullptr;
static Gdiplus::Image* g_uiCar = nullptr;
static Gdiplus::Image* g_uiPackage = nullptr;
static Gdiplus::Image* g_uiFolder = nullptr;
static Gdiplus::Image* g_uiBricks = nullptr;
static Gdiplus::Image* g_thugBalanceMeter = nullptr;
static Gdiplus::Image* g_thugBalanceArrow = nullptr;
static Gdiplus::Image* g_thugBalanceArrowGlow = nullptr;
static Gdiplus::Image* g_thugSpecial = nullptr;
static Gdiplus::Image* g_thugSpecialBar = nullptr;
static Gdiplus::Image* g_thugSpecialBarEnd = nullptr;
static Gdiplus::Image* g_thugMiniScore = nullptr;
static Gdiplus::Image* g_gmodPhysBeam = nullptr;
static Gdiplus::Image* g_gmodPhysBeamActive = nullptr;
static Gdiplus::Image* g_gmodPhysGlow = nullptr;
static Gdiplus::Image* g_physBeamWhite = nullptr;
static Gdiplus::Image* g_physBeamActive = nullptr;
static Gdiplus::Image* g_physGunGlow = nullptr;
static std::unordered_map<UInt32, Gdiplus::Image*> g_propIconCache;

static constexpr int kSpawnWindowWidth = 1140;
static constexpr int kSpawnWindowHeight = 720;
static constexpr int kSpawnCategoryWidth = 248;
static constexpr int kSpawnHeaderHeight = 48;
static constexpr int kSpawnCols = 6;
static constexpr int kSpawnRows = 5;
static constexpr int kSpawnTileW = 145;
static constexpr int kSpawnTileH = 126;
static constexpr int kSpawnPageSize = kSpawnCols * kSpawnRows;

static void RefreshGModSpawnOverlay();
static void HideGModSpawnOverlay();
static void UpdatePhysBeamOverlay();
static void UpdateTHUGHudOverlay();

static Gdiplus::Image* LoadOverlayImage(const wchar_t* fileName)
{
    if (!EnsureGdiPlus()) return nullptr;

    wchar_t path[MAX_PATH] = {};
    _snwprintf_s(path, _countof(path), _TRUNCATE,
        L"Data\\NVSE\\Plugins\\FNVGModTHUG2_UI\\%s", fileName);

    Gdiplus::Image* image = new Gdiplus::Image(path, FALSE);
    if (!image || image->GetLastStatus() != Gdiplus::Ok)
    {
        delete image;
        return nullptr;
    }
    return image;
}

static void EnsureOverlayImages()
{
    if (g_uiContentNormal) return;
    g_uiContentNormal = LoadOverlayImage(L"contenticon-normal.png");
    g_uiContentHover = LoadOverlayImage(L"contenticon-hovered.png");
    g_uiNpc = LoadOverlayImage(L"spawnicon-npc.png");
    g_uiTool = LoadOverlayImage(L"tool.png");
    g_uiGun = LoadOverlayImage(L"gun.png");
    g_uiCar = LoadOverlayImage(L"car.png");
    g_uiPackage = LoadOverlayImage(L"package.png");
    g_uiFolder = LoadOverlayImage(L"folder.png");
    g_uiBricks = LoadOverlayImage(L"bricks.png");

    // Literal HUD textures decoded from the user's THUG2 PS2 assets.
    g_thugBalanceMeter = LoadOverlayImage(L"thug2\\balancemeter.png");
    g_thugBalanceArrow = LoadOverlayImage(L"thug2\\balancearrow.png");
    g_thugBalanceArrowGlow = LoadOverlayImage(L"thug2\\balancearrow_glow.png");
    g_thugSpecial = LoadOverlayImage(L"thug2\\special.png");
    g_thugSpecialBar = LoadOverlayImage(L"thug2\\specialbar.png");
    g_thugSpecialBarEnd = LoadOverlayImage(L"thug2\\specialbar_end.png");
    g_thugMiniScore = LoadOverlayImage(L"thug2\\mini_score_hud.png");
    g_gmodPhysBeam = LoadOverlayImage(L"gmod_physgun\\physbeam_white.png");
    g_gmodPhysBeamActive = LoadOverlayImage(L"gmod_physgun\\physbeam_active_white.png");
    g_gmodPhysGlow = LoadOverlayImage(L"gmod_physgun\\physgun_glow.png");

    // Original Garry's Mod Physgun sprite pixels extracted from garrysmod_dir.vpk.
    g_physBeamWhite = LoadOverlayImage(L"physbeam_white.png");
    g_physBeamActive = LoadOverlayImage(L"physbeam_active_white.png");
    g_physGunGlow = LoadOverlayImage(L"physgun_glow.png");
}

static void DrawOverlayText(HDC dc, const char* text, RECT rc, COLORREF color,
    int fontHeight, int weight = FW_NORMAL, UINT format = DT_LEFT | DT_VCENTER | DT_SINGLELINE)
{
    HFONT font = CreateFontA(
        fontHeight, 0, 0, 0, weight, FALSE, FALSE, FALSE,
        DEFAULT_CHARSET, OUT_DEFAULT_PRECIS, CLIP_DEFAULT_PRECIS,
        CLEARTYPE_QUALITY, DEFAULT_PITCH | FF_DONTCARE, "Tahoma");
    HGDIOBJ oldFont = SelectObject(dc, font);
    SetBkMode(dc, TRANSPARENT);
    SetTextColor(dc, color);
    DrawTextA(dc, text ? text : "", -1, &rc, format);
    SelectObject(dc, oldFont);
    DeleteObject(font);
}

static UInt32 PropIconHash(const char* text)
{
    UInt32 h = 2166136261u;
    if (!text) return h;
    for (const unsigned char* p = reinterpret_cast<const unsigned char*>(text); *p; ++p)
    {
        unsigned char c = *p;
        if (c >= 'A' && c <= 'Z') c = static_cast<unsigned char>(c - 'A' + 'a');
        h ^= c;
        h *= 16777619u;
    }
    return h;
}

static Gdiplus::Image* LoadPropThumbnail(const GModPropDef* prop)
{
    if (!prop || !prop->sourceModel || !*prop->sourceModel)
        return nullptr;
    if (_strnicmp(prop->sourceModel, "npc:", 4) == 0)
        return nullptr;

    const UInt32 hash = PropIconHash(prop->sourceModel);
    const auto found = g_propIconCache.find(hash);
    if (found != g_propIconCache.end())
        return found->second;

    wchar_t relative[96] = {};
    _snwprintf_s(relative, _countof(relative), _TRUNCATE,
        L"propicons\\%08X.png", static_cast<unsigned>(hash));

    Gdiplus::Image* image = LoadOverlayImage(relative);
    g_propIconCache[hash] = image;
    return image;
}

static Gdiplus::Image* IconForBuildProp(const GModPropDef* prop)
{
    if (!prop) return g_uiPackage;
    if (Gdiplus::Image* propIcon = LoadPropThumbnail(prop))
        return propIcon;
    if (prop->sourceModel && _strnicmp(prop->sourceModel, "npc:", 4) == 0)
        return g_uiNpc;
    if (prop->category && strstr(prop->category, "Vehicle"))
        return g_uiCar;
    if (prop->category && (strstr(prop->category, "Weapon") || strstr(prop->category, "Items")))
        return g_uiGun;
    if (prop->category && strstr(prop->category, "Builder"))
        return g_uiTool;
    return g_uiPackage ? g_uiPackage : g_uiBricks;
}

static void SetToolModeFromSpawnMenu(int index)
{
    if (index < 0 ||
        index >= static_cast<int>(sizeof(kGModToolDefs) / sizeof(kGModToolDefs[0])))
        return;

    if (g_toolModeIndex != static_cast<UInt32>(index))
    {
        g_toolModeIndex = static_cast<UInt32>(index);
        g_toolgunEnabled = true;
        PlayGModUISound("ui_hover", "fx\\rem\\gmod\\garrysmod\\ui_hover.wav");
        _MESSAGE("[GMOD-TOOL] spawn menu selected %s", kGModToolDefs[g_toolModeIndex].id);
    }
}

static int ToolSlotFromPoint(int x, int y)
{
    if (x < 6 || x >= kSpawnCategoryWidth - 6)
        return -1;
    if (y >= kSpawnHeaderHeight + 34 && y < kSpawnHeaderHeight + 56)
        return kToolDuplicatorIndex;
    if (y >= kSpawnHeaderHeight + 58 && y < kSpawnHeaderHeight + 80)
        return kToolRemoverIndex;
    return -1;
}

static void EnsureSelectedCategoryVisible()
{
    const int categoryCount = static_cast<int>(GetBuildCategoryCount());
    const int visible = (kSpawnWindowHeight - kSpawnCategoryListTop - 6) / 22;
    if (categoryCount <= visible)
    {
        g_spawnCategoryScroll = 0;
        return;
    }

    const int selected = static_cast<int>(g_buildMenu.categoryIndex);
    if (selected < g_spawnCategoryScroll)
        g_spawnCategoryScroll = selected;
    if (selected >= g_spawnCategoryScroll + visible)
        g_spawnCategoryScroll = selected - visible + 1;

    const int maxScroll = categoryCount - visible;
    if (g_spawnCategoryScroll < 0) g_spawnCategoryScroll = 0;
    if (g_spawnCategoryScroll > maxScroll) g_spawnCategoryScroll = maxScroll;
}

static void PaintGModSpawnMenu(HWND hwnd, HDC dc)
{
    EnsureOverlayImages();
    EnsureSelectedCategoryVisible();

    RECT client = {};
    GetClientRect(hwnd, &client);

    HBRUSH back = CreateSolidBrush(RGB(232, 232, 232));
    FillRect(dc, &client, back);
    DeleteObject(back);

    RECT header = {0, 0, client.right, kSpawnHeaderHeight};
    HBRUSH headerBrush = CreateSolidBrush(RGB(52, 56, 60));
    FillRect(dc, &header, headerBrush);
    DeleteObject(headerBrush);

    RECT title = {18, 0, 460, kSpawnHeaderHeight};
    DrawOverlayText(dc, "Garry's Mod  |  Spawn Menu", title, RGB(245,245,245), 22, FW_BOLD);

    const GModPropCategoryRange* category = GetSelectedBuildCategory();
    char countText[160] = {};
    if (category)
        std::snprintf(countText, sizeof(countText), "%s  |  %u items",
            category->name, static_cast<unsigned>(category->count));
    RECT headerRight = {500, 0, client.right - 16, kSpawnHeaderHeight};
    DrawOverlayText(dc, countText, headerRight, RGB(205,210,215), 16, FW_NORMAL, DT_RIGHT | DT_VCENTER | DT_SINGLELINE);

    RECT categoryPanel = {0, kSpawnHeaderHeight, kSpawnCategoryWidth, client.bottom};
    HBRUSH catBrush = CreateSolidBrush(RGB(205, 208, 211));
    FillRect(dc, &categoryPanel, catBrush);
    DeleteObject(catBrush);

    RECT toolLabel = {12, kSpawnHeaderHeight + 4, kSpawnCategoryWidth - 8, kSpawnHeaderHeight + 30};
    DrawOverlayText(dc, "Tools", toolLabel, RGB(45,45,45), 18, FW_BOLD);

    const struct ToolButton { int index; const char* name; int y; } toolButtons[] = {
        { kToolDuplicatorIndex, "Duplicator", kSpawnHeaderHeight + 34 },
        { kToolRemoverIndex, "Remover", kSpawnHeaderHeight + 58 }
    };
    for (const auto& tool : toolButtons)
    {
        RECT rr = {6, tool.y, kSpawnCategoryWidth - 6, tool.y + 22};
        const bool selected = static_cast<int>(g_toolModeIndex) == tool.index;
        const bool hovered = g_spawnHoveredTool == tool.index;
        if (selected || hovered)
        {
            HBRUSH sel = CreateSolidBrush(RGB(79, 143, 188));
            FillRect(dc, &rr, sel);
            DeleteObject(sel);
        }
        if (g_uiTool)
        {
            Gdiplus::Graphics g(dc);
            g.DrawImage(g_uiTool, 9, tool.y + 3, 16, 16);
        }
        RECT tx = {30, tool.y, kSpawnCategoryWidth - 10, tool.y + 22};
        DrawOverlayText(dc, tool.name, tx,
            selected || hovered ? RGB(255,255,255) : RGB(42,42,42),
            14, selected ? FW_BOLD : FW_NORMAL);
    }

    RECT catLabel = {12, kSpawnHeaderHeight + 86, kSpawnCategoryWidth - 8, kSpawnHeaderHeight + 112};
    DrawOverlayText(dc, "Browse", catLabel, RGB(45,45,45), 18, FW_BOLD);

    const int visibleCategories = (kSpawnWindowHeight - kSpawnCategoryListTop - 6) / 22;
    const int categoryCount = static_cast<int>(GetBuildCategoryCount());
    for (int row = 0; row < visibleCategories; ++row)
    {
        const int idx = g_spawnCategoryScroll + row;
        if (idx >= categoryCount) break;

        const int y = kSpawnCategoryListTop + row * 22;
        RECT rr = {6, y, kSpawnCategoryWidth - 6, y + 21};
        if (idx == static_cast<int>(g_buildMenu.categoryIndex))
        {
            HBRUSH sel = CreateSolidBrush(RGB(79, 143, 188));
            FillRect(dc, &rr, sel);
            DeleteObject(sel);
        }

        const GModPropCategoryRange& c = kGModPropCategories[idx];
        char line[128] = {};
        std::snprintf(line, sizeof(line), "%s  (%u)", c.name, static_cast<unsigned>(c.count));
        RECT tx = {28, y, kSpawnCategoryWidth - 10, y + 21};
        DrawOverlayText(dc, line, tx,
            idx == static_cast<int>(g_buildMenu.categoryIndex) ? RGB(255,255,255) : RGB(42,42,42),
            14, idx == static_cast<int>(g_buildMenu.categoryIndex) ? FW_BOLD : FW_NORMAL);

        if (g_uiFolder)
        {
            Gdiplus::Graphics g(dc);
            g.DrawImage(g_uiFolder, 9, y + 2, 16, 16);
        }
    }

    if (!category || !category->count) return;

    const UInt32 pageStart = (g_buildMenu.itemIndex / kSpawnPageSize) * kSpawnPageSize;
    for (int slot = 0; slot < kSpawnPageSize; ++slot)
    {
        const UInt32 itemOffset = pageStart + slot;
        if (itemOffset >= category->count) break;

        const int col = slot % kSpawnCols;
        const int row = slot / kSpawnCols;
        const int x = kSpawnCategoryWidth + 16 + col * kSpawnTileW;
        const int y = kSpawnHeaderHeight + 12 + row * kSpawnTileH;
        RECT tile = {x, y, x + kSpawnTileW - 8, y + kSpawnTileH - 8};

        const bool selected = itemOffset == g_buildMenu.itemIndex;
        const bool hovered = slot == g_spawnHoveredItem;

        Gdiplus::Graphics g(dc);
        Gdiplus::Image* tileImage = (selected || hovered) && g_uiContentHover
            ? g_uiContentHover : g_uiContentNormal;
        if (tileImage)
            g.DrawImage(tileImage, static_cast<INT>(tile.left), static_cast<INT>(tile.top),
                static_cast<INT>(tile.right - tile.left), static_cast<INT>(tile.bottom - tile.top));
        else
        {
            HBRUSH b = CreateSolidBrush(selected || hovered ? RGB(180,205,225) : RGB(248,248,248));
            FillRect(dc, &tile, b);
            DeleteObject(b);
        }

        const UInt32 defIndex = category->start + itemOffset;
        const UInt32 totalDefs = static_cast<UInt32>(sizeof(kGModPropDefs) / sizeof(kGModPropDefs[0]));
        if (defIndex >= totalDefs) continue;
        const GModPropDef* prop = &kGModPropDefs[defIndex];

        Gdiplus::Image* icon = IconForBuildProp(prop);
        if (icon)
            g.DrawImage(icon, x + 39, y + 16, 52, 52);

        RECT label = {x + 8, y + 72, x + kSpawnTileW - 16, y + kSpawnTileH - 15};
        DrawOverlayText(dc, prop->displayName, label, RGB(35,35,35), 13,
            selected ? FW_BOLD : FW_NORMAL,
            DT_CENTER | DT_WORDBREAK | DT_END_ELLIPSIS);
    }

    char pageText[128] = {};
    const UInt32 pageNo = pageStart / kSpawnPageSize + 1;
    const UInt32 pageCount = (category->count + kSpawnPageSize - 1) / kSpawnPageSize;
    std::snprintf(pageText, sizeof(pageText),
        "Page %u / %u   |   Hover Duplicator/Remover to arm Tool Gun   |   Click: spawn   |   Z: undo",
        static_cast<unsigned>(pageNo), static_cast<unsigned>(pageCount));
    RECT footer = {kSpawnCategoryWidth + 16, client.bottom - 28, client.right - 12, client.bottom - 4};
    DrawOverlayText(dc, pageText, footer, RGB(55,55,55), 14, FW_NORMAL);
}

static int SpawnSlotFromPoint(int x, int y)
{
    if (x < kSpawnCategoryWidth + 16 || y < kSpawnHeaderHeight + 12)
        return -1;
    const int relX = x - (kSpawnCategoryWidth + 16);
    const int relY = y - (kSpawnHeaderHeight + 12);
    const int col = relX / kSpawnTileW;
    const int row = relY / kSpawnTileH;
    if (col < 0 || col >= kSpawnCols || row < 0 || row >= kSpawnRows)
        return -1;
    const int insideX = relX % kSpawnTileW;
    const int insideY = relY % kSpawnTileH;
    if (insideX >= kSpawnTileW - 8 || insideY >= kSpawnTileH - 8)
        return -1;
    return row * kSpawnCols + col;
}

static LRESULT CALLBACK GModSpawnOverlayWndProc(HWND hwnd, UINT msg, WPARAM wParam, LPARAM lParam)
{
    switch (msg)
    {
    case WM_ERASEBKGND:
        return 1;
    case WM_PAINT:
    {
        PAINTSTRUCT ps = {};
        HDC dc = BeginPaint(hwnd, &ps);
        RECT rc = {};
        GetClientRect(hwnd, &rc);

        HDC mem = CreateCompatibleDC(dc);
        HBITMAP bmp = CreateCompatibleBitmap(dc, rc.right, rc.bottom);
        HGDIOBJ oldBmp = SelectObject(mem, bmp);

        PaintGModSpawnMenu(hwnd, mem);
        BitBlt(dc, 0, 0, rc.right, rc.bottom, mem, 0, 0, SRCCOPY);

        SelectObject(mem, oldBmp);
        DeleteObject(bmp);
        DeleteDC(mem);
        EndPaint(hwnd, &ps);
        return 0;
    }
    case WM_MOUSEMOVE:
    {
        const int x = GET_X_LPARAM(lParam);
        const int y = GET_Y_LPARAM(lParam);
        const int toolHover = ToolSlotFromPoint(x, y);
        if (toolHover != g_spawnHoveredTool)
        {
            g_spawnHoveredTool = toolHover;
            if (toolHover >= 0)
                SetToolModeFromSpawnMenu(toolHover);
            InvalidateRect(hwnd, nullptr, FALSE);
        }

        const int hover = SpawnSlotFromPoint(x, y);
        if (hover != g_spawnHoveredItem)
        {
            g_spawnHoveredItem = hover;
            InvalidateRect(hwnd, nullptr, FALSE);
        }
        return 0;
    }
    case WM_MOUSEWHEEL:
    {
        const short delta = GET_WHEEL_DELTA_WPARAM(wParam);
        POINT p = {GET_X_LPARAM(lParam), GET_Y_LPARAM(lParam)};
        ScreenToClient(hwnd, &p);

        if (p.x < kSpawnCategoryWidth)
        {
            ChangeBuildCategory(delta > 0 ? -1 : 1);
        }
        else
        {
            const GModPropCategoryRange* cat = GetSelectedBuildCategory();
            if (cat && cat->count)
            {
                int next = static_cast<int>(g_buildMenu.itemIndex) + (delta > 0 ? -kSpawnPageSize : kSpawnPageSize);
                if (next < 0) next = 0;
                if (next >= static_cast<int>(cat->count))
                    next = static_cast<int>(cat->count) - 1;
                g_buildMenu.itemIndex = static_cast<UInt32>(next);
            }
        }
        InvalidateRect(hwnd, nullptr, FALSE);
        return 0;
    }
    case WM_LBUTTONDOWN:
    {
        const int x = GET_X_LPARAM(lParam);
        const int y = GET_Y_LPARAM(lParam);

        const int toolSlot = ToolSlotFromPoint(x, y);
        if (toolSlot >= 0)
        {
            SetToolModeFromSpawnMenu(toolSlot);
            InvalidateRect(hwnd, nullptr, FALSE);
            return 0;
        }

        if (x < kSpawnCategoryWidth && y >= kSpawnCategoryListTop)
        {
            const int row = (y - kSpawnCategoryListTop) / 22;
            const int idx = g_spawnCategoryScroll + row;
            if (idx >= 0 && idx < static_cast<int>(GetBuildCategoryCount()))
            {
                g_buildMenu.categoryIndex = static_cast<UInt32>(idx);
                g_buildMenu.itemIndex = 0;
                PlayGModUISound("ui_hover", "fx\\rem\\gmod\\garrysmod\\ui_hover.wav");
                InvalidateRect(hwnd, nullptr, FALSE);
            }
            return 0;
        }

        const int slot = SpawnSlotFromPoint(x, y);
        if (slot >= 0)
        {
            const GModPropCategoryRange* cat = GetSelectedBuildCategory();
            if (cat)
            {
                const UInt32 pageStart = (g_buildMenu.itemIndex / kSpawnPageSize) * kSpawnPageSize;
                const UInt32 item = pageStart + static_cast<UInt32>(slot);
                if (item < cat->count)
                {
                    g_buildMenu.itemIndex = item;
                    SpawnSelectedBuildProp();
                    InvalidateRect(hwnd, nullptr, FALSE);
                }
            }
        }
        return 0;
    }
    default:
        break;
    }
    return DefWindowProc(hwnd, msg, wParam, lParam);
}

static void PaintPhysBeam(HWND hwnd, HDC dc)
{
    RECT r = {};
    GetClientRect(hwnd, &r);
    HBRUSH key = CreateSolidBrush(RGB(1, 2, 3));
    FillRect(dc, &r, key);
    DeleteObject(key);

    if (!(g_physgunEnabled || g_weaponPhysgunActive) || !g_heldRef)
        return;

    const int sx = static_cast<int>(r.right * 0.72f);
    const int sy = static_cast<int>(r.bottom * 0.80f);
    const int tx = r.right / 2;
    const int ty = r.bottom / 2;

    Gdiplus::Graphics g(dc);
    const float dx = static_cast<float>(tx - sx);
    const float dy = static_cast<float>(ty - sy);
    const float len = std::sqrt(dx * dx + dy * dy);
    if (len > 1.0f)
    {
        const float px = (-dy / len) * 7.0f;
        const float py = ( dx / len) * 7.0f;
        Gdiplus::PointF quad[3] = {
            Gdiplus::PointF(static_cast<float>(sx) + px, static_cast<float>(sy) + py),
            Gdiplus::PointF(static_cast<float>(tx) + px, static_cast<float>(ty) + py),
            Gdiplus::PointF(static_cast<float>(sx) - px, static_cast<float>(sy) - py)
        };

        Gdiplus::Image* beamImage = g_physBeamActive ? g_physBeamActive : g_physBeamWhite;
        if (beamImage)
        {
            // Source material color-modulates the white beam. Keep GMod's pixels and
            // apply its familiar cyan player color here.
            Gdiplus::ColorMatrix cm = {{
                {0.31f,0,0,0,0},
                {0,0.86f,0,0,0},
                {0,0,1.00f,0,0},
                {0,0,0,1,0},
                {0,0,0,0,1}
            }};
            Gdiplus::ImageAttributes attr;
            attr.SetColorMatrix(&cm);
            g.DrawImage(beamImage, quad, 3,
                0, 0,
                static_cast<INT>(beamImage->GetWidth()),
                static_cast<INT>(beamImage->GetHeight()),
                Gdiplus::UnitPixel, &attr);
        }
    }

    if (g_physGunGlow)
    {
        const int glowSize = 72;
        g.DrawImage(g_physGunGlow,
            tx - glowSize / 2, ty - glowSize / 2,
            glowSize, glowSize);
    }

}

static LRESULT CALLBACK PhysBeamOverlayWndProc(HWND hwnd, UINT msg, WPARAM wParam, LPARAM lParam)
{
    if (msg == WM_ERASEBKGND) return 1;
    if (msg == WM_PAINT)
    {
        PAINTSTRUCT ps = {};
        HDC dc = BeginPaint(hwnd, &ps);
        PaintPhysBeam(hwnd, dc);
        EndPaint(hwnd, &ps);
        return 0;
    }
    return DefWindowProc(hwnd, msg, wParam, lParam);
}

static const char* OverlaySkateStateName(SkateMoveState state)
{
    switch (state)
    {
    case SkateMoveState::Ground: return "GROUND";
    case SkateMoveState::Air: return "AIR";
    case SkateMoveState::Grind: return "GRIND";
    case SkateMoveState::Manual: return "MANUAL";
    case SkateMoveState::Lip: return "LIP";
    case SkateMoveState::Skitch: return "SKITCH";
    default: return "SKATE";
    }
}

static void PaintTHUGHud(HWND hwnd, HDC dc)
{
    RECT r = {};
    GetClientRect(hwnd, &r);
    HBRUSH key = CreateSolidBrush(RGB(1, 2, 3));
    FillRect(dc, &r, key);
    DeleteObject(key);

    if (!g_skate.active) return;

    char combo[160] = {};
    if (g_skate.comboActive)
        std::snprintf(combo, sizeof(combo), "%.0f  x%.2f", g_skate.comboScore, g_skate.comboMultiplier);
    else
        std::snprintf(combo, sizeof(combo), "%.0f", g_skate.totalScore);

    RECT comboRect = {r.right / 2 - 260, 28, r.right / 2 + 260, 88};
    DrawOverlayText(dc, combo, comboRect, RGB(255, 220, 60), 42, FW_BOLD,
        DT_CENTER | DT_VCENTER | DT_SINGLELINE);

    RECT trickRect = {r.right / 2 - 360, 82, r.right / 2 + 360, 120};
    DrawOverlayText(dc,
        g_skate.lastTrick[0] ? g_skate.lastTrick : "THUG2 MODE",
        trickRect, RGB(255,255,255), 22, FW_BOLD,
        DT_CENTER | DT_VCENTER | DT_SINGLELINE);

    char state[128] = {};
    std::snprintf(state, sizeof(state), "%s   SPEED %d%%",
        OverlaySkateStateName(g_skate.moveState),
        static_cast<int>(g_skate.speed01 * 100.0f));
    RECT stateRect = {28, 28, 320, 62};
    DrawOverlayText(dc, state, stateRect, RGB(245,245,245), 18, FW_BOLD);

    Gdiplus::Graphics thugG(dc);

    // Original THUG2 score HUD backing.
    if (g_thugMiniScore)
        thugG.DrawImage(g_thugMiniScore, r.right / 2 - 128, 18, 256, 128);

    // Original THUG2 SPECIAL label/bar/end-cap textures.
    const int specialX = 28;
    const int specialY = r.bottom - 68;
    if (g_thugSpecial)
        thugG.DrawImage(g_thugSpecial, specialX, specialY - 26, 128, 24);
    if (g_thugSpecialBar)
    {
        const int fillW = static_cast<int>(300.0f * g_skate.special01);
        if (fillW > 0)
        {
            const INT srcW = static_cast<INT>(
                g_thugSpecialBar->GetWidth() * g_skate.special01);
            Gdiplus::Rect dest(specialX, specialY, fillW, 20);
            thugG.DrawImage(g_thugSpecialBar, dest,
                0, 0, srcW, static_cast<INT>(g_thugSpecialBar->GetHeight()),
                Gdiplus::UnitPixel);
        }
    }
    if (g_thugSpecialBarEnd)
        thugG.DrawImage(g_thugSpecialBarEnd, specialX + 298, specialY - 6, 24, 32);

    if (g_skate.moveState == SkateMoveState::Grind ||
        g_skate.moveState == SkateMoveState::Manual ||
        g_skate.moveState == SkateMoveState::Lip ||
        g_skate.moveState == SkateMoveState::Skitch)
    {
        const int bx = r.right / 2 - 256;
        const int by = r.bottom - 82;
        if (g_thugBalanceMeter)
            thugG.DrawImage(g_thugBalanceMeter, bx, by, 512, 64);

        const int marker = bx + 256 +
            static_cast<int>(g_skate.balance * 220.0f);
        if (g_thugBalanceArrowGlow)
            thugG.DrawImage(g_thugBalanceArrowGlow, marker - 16, by - 8, 32, 64);
        if (g_thugBalanceArrow)
            thugG.DrawImage(g_thugBalanceArrow, marker - 10, by + 18, 20, 20);
    }

    RECT help = {r.right - 520, r.bottom - 52, r.right - 24, r.bottom - 12};
    DrawOverlayText(dc,
        "SPACE Ollie  |  LMB Flip  |  RMB Grab  |  M Manual  |  G Grind  |  R Exit",
        help, RGB(225,225,225), 14, FW_NORMAL,
        DT_RIGHT | DT_VCENTER | DT_SINGLELINE);
}

static LRESULT CALLBACK THUGHudOverlayWndProc(HWND hwnd, UINT msg, WPARAM wParam, LPARAM lParam)
{
    if (msg == WM_ERASEBKGND) return 1;
    if (msg == WM_PAINT)
    {
        PAINTSTRUCT ps = {};
        HDC dc = BeginPaint(hwnd, &ps);
        PaintTHUGHud(hwnd, dc);
        EndPaint(hwnd, &ps);
        return 0;
    }
    return DefWindowProc(hwnd, msg, wParam, lParam);
}

static bool EnsureOverlayWindowClasses()
{
    if (g_overlayClassesRegistered) return true;

    HINSTANCE hInst = GetModuleHandle(nullptr);

    WNDCLASSW spawn = {};
    spawn.lpfnWndProc = GModSpawnOverlayWndProc;
    spawn.hInstance = hInst;
    spawn.hCursor = LoadCursor(nullptr, IDC_ARROW);
    spawn.lpszClassName = L"FNVGModTHUG2SpawnOverlay";
    if (!RegisterClassW(&spawn) && GetLastError() != ERROR_CLASS_ALREADY_EXISTS)
        return false;

    WNDCLASSW beam = {};
    beam.lpfnWndProc = PhysBeamOverlayWndProc;
    beam.hInstance = hInst;
    beam.hCursor = LoadCursor(nullptr, IDC_ARROW);
    beam.lpszClassName = L"FNVGModTHUG2PhysBeamOverlay";
    if (!RegisterClassW(&beam) && GetLastError() != ERROR_CLASS_ALREADY_EXISTS)
        return false;

    WNDCLASSW thug = {};
    thug.lpfnWndProc = THUGHudOverlayWndProc;
    thug.hInstance = hInst;
    thug.hCursor = LoadCursor(nullptr, IDC_ARROW);
    thug.lpszClassName = L"FNVGModTHUG2SkateHudOverlay";
    if (!RegisterClassW(&thug) && GetLastError() != ERROR_CLASS_ALREADY_EXISTS)
        return false;

    g_overlayClassesRegistered = true;
    return true;
}

static HWND ResolveFalloutWindow()
{
    if (g_falloutGameWindow && IsWindow(g_falloutGameWindow))
        return g_falloutGameWindow;

    HWND fg = GetForegroundWindow();
    if (fg)
        g_falloutGameWindow = fg;
    return g_falloutGameWindow;
}

static void PositionOverlayOverGame(HWND hwnd, int width, int height)
{
    HWND game = ResolveFalloutWindow();
    if (!game || !hwnd) return;

    RECT wr = {};
    GetWindowRect(game, &wr);
    const int gameW = wr.right - wr.left;
    const int gameH = wr.bottom - wr.top;

    const int x = wr.left + (gameW - width) / 2;
    const int y = wr.top + (gameH - height) / 2;
    SetWindowPos(hwnd, HWND_TOPMOST, x, y, width, height,
        SWP_NOACTIVATE | SWP_SHOWWINDOW);
}

static void ShowGModSpawnOverlay()
{
    if (!EnsureOverlayWindowClasses()) return;
    EnsureOverlayImages();

    HWND game = ResolveFalloutWindow();
    if (!g_gmodSpawnWindow)
    {
        g_gmodSpawnWindow = CreateWindowExW(
            WS_EX_TOPMOST | WS_EX_TOOLWINDOW | WS_EX_NOACTIVATE,
            L"FNVGModTHUG2SpawnOverlay",
            L"Garry's Mod Spawn Menu",
            WS_POPUP,
            0, 0, kSpawnWindowWidth, kSpawnWindowHeight,
            game, nullptr, GetModuleHandle(nullptr), nullptr);
    }

    if (g_gmodSpawnWindow)
    {
        PositionOverlayOverGame(g_gmodSpawnWindow, kSpawnWindowWidth, kSpawnWindowHeight);
        ShowWindow(g_gmodSpawnWindow, SW_SHOWNOACTIVATE);
        InvalidateRect(g_gmodSpawnWindow, nullptr, TRUE);
    }
}

static void HideGModSpawnOverlay()
{
    if (g_gmodSpawnWindow)
        ShowWindow(g_gmodSpawnWindow, SW_HIDE);
}

static void RefreshGModSpawnOverlay()
{
    if (g_gmodSpawnWindow && IsWindowVisible(g_gmodSpawnWindow))
        InvalidateRect(g_gmodSpawnWindow, nullptr, FALSE);
}

static void UpdatePhysBeamOverlay()
{
    const bool shouldShow =
        !g_buildMenu.open &&
        (g_physgunEnabled || g_weaponPhysgunActive) &&
        g_heldRef != nullptr;

    if (!shouldShow)
    {
        if (g_physBeamWindow)
            ShowWindow(g_physBeamWindow, SW_HIDE);
        return;
    }

    if (!EnsureOverlayWindowClasses()) return;

    HWND game = ResolveFalloutWindow();
    if (!game) return;

    RECT wr = {};
    GetWindowRect(game, &wr);
    const int w = wr.right - wr.left;
    const int h = wr.bottom - wr.top;

    if (!g_physBeamWindow)
    {
        g_physBeamWindow = CreateWindowExW(
            WS_EX_TOPMOST | WS_EX_TOOLWINDOW | WS_EX_NOACTIVATE |
            WS_EX_TRANSPARENT | WS_EX_LAYERED,
            L"FNVGModTHUG2PhysBeamOverlay",
            L"",
            WS_POPUP,
            wr.left, wr.top, w, h,
            game, nullptr, GetModuleHandle(nullptr), nullptr);

        if (g_physBeamWindow)
            SetLayeredWindowAttributes(g_physBeamWindow, RGB(1,2,3), 255, LWA_COLORKEY);
    }

    if (g_physBeamWindow)
    {
        SetWindowPos(g_physBeamWindow, HWND_TOPMOST, wr.left, wr.top, w, h,
            SWP_NOACTIVATE | SWP_SHOWWINDOW);
        InvalidateRect(g_physBeamWindow, nullptr, TRUE);
    }
}

static void UpdateTHUGHudOverlay()
{
    if (!g_skate.active)
    {
        if (g_thugHudWindow)
            ShowWindow(g_thugHudWindow, SW_HIDE);
        return;
    }

    if (!EnsureOverlayWindowClasses()) return;
    HWND game = ResolveFalloutWindow();
    if (!game) return;

    RECT wr = {};
    GetWindowRect(game, &wr);
    const int w = wr.right - wr.left;
    const int h = wr.bottom - wr.top;

    if (!g_thugHudWindow)
    {
        g_thugHudWindow = CreateWindowExW(
            WS_EX_TOPMOST | WS_EX_TOOLWINDOW | WS_EX_NOACTIVATE |
            WS_EX_TRANSPARENT | WS_EX_LAYERED,
            L"FNVGModTHUG2SkateHudOverlay",
            L"",
            WS_POPUP,
            wr.left, wr.top, w, h,
            game, nullptr, GetModuleHandle(nullptr), nullptr);

        if (g_thugHudWindow)
            SetLayeredWindowAttributes(g_thugHudWindow, RGB(1,2,3), 255, LWA_COLORKEY);
    }

    if (g_thugHudWindow)
    {
        SetWindowPos(g_thugHudWindow, HWND_TOPMOST, wr.left, wr.top, w, h,
            SWP_NOACTIVATE | SWP_SHOWWINDOW);
        InvalidateRect(g_thugHudWindow, nullptr, TRUE);
    }
}