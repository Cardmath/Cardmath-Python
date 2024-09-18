from creditcard.enums import RewardUnit

def test_RewardUnit_get_value():
    rewards = RewardUnit.AA_ADVANTAGE_MILES
    assert rewards.value == "American Airlines AAdvantage Miles"
    assert rewards.name == "AA_ADVANTAGE_MILES"
    assert isinstance(RewardUnit.get_value(rewards), float)