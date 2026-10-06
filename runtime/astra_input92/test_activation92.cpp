#include "skate_activation_gate92.h"
#include <cstdio>
#include <cstdlib>
static unsigned checks = 0;
static void check(bool value, const char* label)
{
    ++checks;
    if (!value) { std::fprintf(stderr, "FAIL: %s\n", label); std::exit(1); }
}
static void normal_click(SkateActivationGate92& g)
{
    check(!g.Sample(true,false), "release does not activate");
    check(g.Sample(true,true), "fresh press activates");
    check(!g.Sample(true,true), "held press does not repeat");
}
int main()
{
    SkateActivationGate92 g;
    check(!g.Sample(true,false) && !g.Sample(true,true), "startup cannot activate");
    g.WorldAvailable();
    check(!g.Sample(true,true), "load-held click blocked");
    normal_click(g);
    for (int reason=0; reason<7; ++reason) {
        // Focus loss, Q menu, vehicle, missing player/cell, context unavailable,
        // weapon unequip and already-active skate mode all revoke eligibility.
        g.Sample(true,false);
        check(!g.Sample(false,false), "ineligible release cannot arm");
        check(!g.Sample(true,true), "resume-held click blocked");
        normal_click(g);
    }
    g.Sample(true,false);
    g.Suspend();
    check(!g.Sample(true,true), "early return revokes previous arm");
    normal_click(g);
    g.WorldUnavailable();
    check(!g.Sample(true,false) && !g.Sample(true,true), "preload/title forbids entry");
    g.Suspend();
    check(!g.Sample(true,true), "suspend cannot unlock world");
    g.WorldAvailable();
    check(!g.Sample(true,true), "new world requires release");
    normal_click(g);
    // Exhaust all seven-event traces from six input/lifecycle events.
    // Safety property: activation requires an uninterrupted eligible release
    // since the most recent world/ownership boundary, followed by a press.
    unsigned traces=1; for(int i=0;i<7;++i) traces*=6;
    for(unsigned trace=0;trace<traces;++trace) {
        SkateActivationGate92 x;
        unsigned encoded=trace;
        bool world=false, released=false;
        for(int step=0;step<7;++step) {
            const unsigned event=encoded%6; encoded/=6;
            if(event==0) { x.WorldUnavailable(); world=false; released=false; }
            else if(event==1) { x.WorldAvailable(); world=true; released=false; }
            else if(event==2) { x.Suspend(); released=false; }
            else if(event==3) { check(!x.Sample(false,false),"blocked sample"); released=false; }
            else if(event==4) { check(!x.Sample(true,false),"release sample"); released=world; }
            else {
                const bool fired=x.Sample(true,true);
                check(fired==(world && released),"trace eligible edge contract");
                released=false;
            }
        }
    }
    std::printf("PASS: %u checks; %u exhaustive lifecycle/input traces\n",checks,traces);
}
