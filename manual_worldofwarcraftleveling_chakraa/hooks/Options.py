# Object classes from AP that represent different types of options that you can create
from Options import Option, FreeText, NumericOption, Toggle, DefaultOnToggle, Choice, TextChoice, Range, NamedRange, OptionGroup, PerGameCommonOptions
# These helper methods allow you to determine if an option has been set, or what its value is, for any player in the multiworld
from ..Helpers import is_option_enabled, get_option_value
from typing import Type, Any


####################################################################
# NOTE: At the time that options are created, Manual has no concept of the multiworld or its own world.
#       Options are defined before the world is even created.
#
# Example of creating your own option:
#
#   class MakeThePlayerOP(Toggle):
#       """Should the player be overpowered? Probably not, but you can choose for this to do... something!"""
#       display_name = "Make me OP"
#
#   options["make_op"] = MakeThePlayerOP
#
#
# Then, to see if the option is set, you can call is_option_enabled or get_option_value.
#####################################################################


# To add an option, use the before_options_defined hook below and something like this:
#   options["total_characters_to_win_with"] = TotalCharactersToWinWith
#
class GoldHuntAmount(Range):
    """If you have selected the Gold Hunt Goal, choose how much Gold you need to find in the pool to win."""
    display_name = "Gold amount"
    range_start = 1
    range_end = 10
    default = 10

class Expansion(Choice):
    """This will affect the items/locations in the randomizer to match what max level you want to reach.
    vanilla = Level 60
    the_burning_crusade = Level 70
    wrath_of_the_lich_king = Level 80
    cataclysm = Level 85
    mists_of_pandaria = Level 90"""
    display_name = """Selected Expansion"""
    option_vanilla = 0
    option_the_burning_crusade = 1
    option_wrath_of_the_lich_king = 2
    option_cataclysm = 3
    option_mists_of_pandaria = 4
    default = 4

class Faction(Choice):
    """Choose your character faction. (affects which zones are available for you to quest in)"""
    display_name = """Character faction"""
    option_alliance = 0
    option_horde = 1
    default = "random"

class RandomizeClass(Toggle):
    """If set to 'true', you will be given a random class for you to play. You can see the received class in the Manual client."""
    display_name = """Randomize Starting Class"""
    default = False
    
class LevelItems(Choice):
    """Progressive will add multiple Progressive Levels to the pool and replace the normal "Maximum Level X" items."""
    display_name = """Progressive or Sequential"""
    option_sequential = 0
    option_progressive = 1
    default = 1

class EasierTransitions(Choice):
    """Setting it to true will make it that the logic will always expect 2 zones for each level bracket (eg: 10-20) and the first zone of each expansion to be received before allowing progression.
    This will make it easier to quest in logic by allowing you more zone choices for your level."""
    display_name = """Easier Transitions"""
    option_false = 0
    option_true = 1
    default = 0

class PreOrPostCataclysm(Choice):
    """Select whether you want to quest in the pre-cataclysm or post-cataclysm versions of zones affected by the Cataclysm expansion in the pool.
    Setting this option to Pre-Cataclysm will make it so that zones like Stranglethorn Vale, Desolace, Feralas, and Thousand Needles are in their original states.
    If you choose your Goal to be Vanilla, The Burning Crusade, or Wrath of the Lich King, you can still choose Post-Cataclysm as your option, if you are playing Cataclysm or Mists of Pandaria game versions.
    ## WARNING ## If you choose your Goal to be either Cataclysm or Mists of Pandaria, you will automatically be set to Post-Cataclysm, as those expansions assume the world has already been changed by Cataclysm."""
    display_name = """Pre or Post Cataclysm"""
    option_pre_cataclysm = 0
    option_post_cataclysm = 1
    default = 1

# This is called before any manual options are defined, in case you want to define your own with a clean slate or let Manual define over them
def before_options_defined(options: dict[str, Type[Option[Any]]]) -> dict[str, Type[Option[Any]]]:
    options["gold_hunt_amount"] = GoldHuntAmount
    options["expansion"] = Expansion
    options["pre_or_post_cataclysm"] = PreOrPostCataclysm
    options["faction"] = Faction
    options["randomize_class"] = RandomizeClass
    options["level_items"] = LevelItems
    options["easier_transitions"] = EasierTransitions
    return options

# This is called after any manual options are defined, in case you want to see what options are defined or want to modify the defined options
def after_options_defined(options: Type[PerGameCommonOptions]):
    # To access a modifiable version of options check the dict in options.type_hints
    # For example if you want to change DLC_enabled's display name you would do:
    # options.type_hints["DLC_enabled"].display_name = "New Display Name"

    #  Here's an example on how to add your aliases to the generated goal
    # options.type_hints['goal'].aliases.update({"example": 0, "second_alias": 1})
    # options.type_hints['goal'].options.update({"example": 0, "second_alias": 1})  #for an alias to be valid it must also be in options

    options.type_hints["goal"].__doc__ = """Select your goal for the randomizer.
    Leveling: Reach the maximum level for your selected expansion. Define the expansion with the 'expansion' option.
    Gold Hunt: Find a set amount of Gold in the item pool to win. Define the amount of Gold needed with the 'gold_hunt_amount' option."""    
    options.type_hints["goal"].default = 0
    options.type_hints["goal"].display_name = "Selected Goal"
    options.type_hints["include_dungeons"].__doc__ = """If set to 'true', this will add all the various leveling dungeons as Filler items. This has no effect on logic; only Maximum Level and Zone Items do."""
    options.type_hints["include_dungeons"].default = False
    options.type_hints["include_dungeons"].display_name = "Include Dungeons"
    return options

# Use this Hook if you want to add your Option to an Option group (existing or not)
def before_option_groups_created(groups: dict[str, list[Type[Option[Any]]]]) -> dict[str, list[Type[Option[Any]]]]:
    # Uses the format groups['GroupName'] = [TotalCharactersToWinWith]
    return groups

def after_option_groups_created(groups: list[OptionGroup]) -> list[OptionGroup]:
    return groups
