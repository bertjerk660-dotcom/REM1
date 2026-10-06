// FNV 1.4.0.525 scene adapter. IDA 6.8 evidence: checkpoint 90.
// Deliberately separate from the obsolete OBSE-derived NiObjects virtual declarations.
struct FNVTransform90
{
    NiMatrix33 rotate;
    NiVector3 translate;
    float scale;
};
static_assert(sizeof(FNVTransform90)==0x34,"FNV transform includes scale");
static FNVTransform90& FNVLocal90(NiAVObject* object)
{
    return *reinterpret_cast<FNVTransform90*>(reinterpret_cast<unsigned char*>(object)+0x34);
}
static bool FNVKnownNode90(NiNode* root)
{
    if (!root) return false;
    const UInt32* vt=*reinterpret_cast<const UInt32* const*>(root);
    return vt[0x27]==0xA5E560 && vt[0x29]==0xA5DD70;
}
static NiObjectNET* FNVFindNode90(NiNode* root,const char* name)
{
    if (!name || !FNVKnownNode90(root)) return nullptr;
    // The search compares interned handles; passing a C string is ABI-incompatible.
    const char* handle=nullptr;
    typedef void (__thiscall* Construct)(void*,const char*);
    typedef void (__thiscall* Destroy)(void*);
    reinterpret_cast<Construct>(0x438170)(&handle,name);
    typedef NiObjectNET* (__thiscall* Find)(NiNode*,const char* const*);
    const UInt32* vt=*reinterpret_cast<const UInt32* const*>(root);
    NiObjectNET* result=reinterpret_cast<Find>(vt[0x27])(root,&handle);
    reinterpret_cast<Destroy>(0x4381B0)(&handle);
    return result;
}
static bool FNVRefreshPose90(NiNode* root)
{
    if (!FNVKnownNode90(root)) return false;
    // Observed update context: time at 0, controller enable byte at 4.
    // Full subtype context semantics remain a runtime validation gate.
    struct UpdateContext { float time; unsigned char flags[12]; } context={};
    typedef void (__thiscall* DownwardPass)(NiNode*,void*,UInt32);
    const UInt32* vt=*reinterpret_cast<const UInt32* const*>(root);
    reinterpret_cast<DownwardPass>(vt[0x29])(root,&context,0);
    return true;
}
