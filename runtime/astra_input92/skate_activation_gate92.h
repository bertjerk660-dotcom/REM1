#pragma once
// Host input ownership only; no THUG2 physics or animation behavior is synthesized.
// A context interruption always requires a released sample in eligible gameplay.
class SkateActivationGate92
{
public:
    enum class Phase { WorldUnavailable, AwaitRelease, Armed };
    void WorldUnavailable() { phase_ = Phase::WorldUnavailable; }
    void WorldAvailable() { phase_ = Phase::AwaitRelease; }
    void Suspend()
    {
        if (phase_ != Phase::WorldUnavailable) phase_ = Phase::AwaitRelease;
    }
    bool Sample(bool eligible, bool attackDown)
    {
        if (phase_ == Phase::WorldUnavailable) return false;
        if (!eligible) { Suspend(); return false; }
        if (!attackDown) { phase_ = Phase::Armed; return false; }
        const bool requested = phase_ == Phase::Armed;
        phase_ = Phase::AwaitRelease; // consumes the edge even if entry fails
        return requested;
    }
private:
    Phase phase_ = Phase::WorldUnavailable;
};
