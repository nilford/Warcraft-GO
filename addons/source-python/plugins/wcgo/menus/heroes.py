"""Provides the hero menu instances."""

# Python 3
import collections

# Source.Python
import menus

# Warcraft: GO
import wcgo.configs as cfg
from wcgo.menus.extensions import PagedMenu
import wcgo.menus.strings as strings
from wcgo.player import Player

"""Owned hero display instance."""

def _owned_hero_menu_build(menu, index):
    player = Player(index)
    hero = menu.hero
    levelinfo = '{hero.level}/{hero.max_level}'.format(hero=hero)
        if not hero.is_max_level() else 'Maxed'

    # Construct menu ready for addition of items
    menu.title = strings.OWNED_HEROES_MENU['Hero'].format(
        hero=hero.name,
        levelinfo=levelinfo)
    menu.description = hero.description
    menu.clear()

    for num, skill in enumerate(hero.skills, start=1):
        # Check whether reset should be added
        if num % 6 == 0:
            option = menus.PagedOption(
                strings.OWNED_HEROES_MENU['Change'],
                1)
            menu.append(option)

        # Append the skill in iteration to the menu
        levelinfo = '{skill.level}/{skill.max_level}'.format(skill=skill)
            if not skill.is_max_level() else 'Maxed'
        option = menus.PagedOption(
            strings.OWNED_HEROES_MENU['Skill'].format(skill=skill.name, levelinfo=levelinfo, description=skill.description),
            None)
        menu.append(option)

def _owned_hero_menu_select(menu, index, choice):
    player = Player(index)
    if choice.value is 1:
        player.hero = choice.value
    else:
        return menu

owned_hero_menu = PagedMenu(
    build_callback= _owned_hero_menu_build,
    select_callback=_owned_hero_menu_select)

"""Owned heroes selection menu instance."""

def _owned_heroes_menu_build(menu, index):
    player = Player(index)

    menu.clear()
    for hero in menu.heroes:
        option = PagedOption(hero.name, hero)
        menu.append(option)

def _owned_heroes_menu_select(menu, index, choice):
    owned_hero_menu.hero = choice.value
    return owned_hero_menu

owned_heroes_menu = PagedMenu(
    build_callback= _owned_heroes_menu_build,
    select_callback=_owned_heroes_menu_select)

"""Owned hero category menu instance."""

def _owned_categories_menu_build(menu, index):
    player = Player(index)

    # Retrieve all heroes available for player
    categories = collections.defaultdict(list)
    for hero in player.heroes:
        categories[hero.category].append(hero)

    menu.clear()

    # Construct menu from categories
    for category in categories:
        option = PagedOption(category, (category, categories[category]))
        menu.append(option)

def _owned_categories_menu_select(menu, index, choice):
    owned_heroes_menu.title, owned_heroes_menu.heroes = choice.value
    return owned_heroes_menu

owned_categories_menu = PagedMenu(
    title=strings.OWNED_HEROES_MENU['Title'],
    build_callback= _owned_categories_menu_build,
    select_callback=_owned_categories_menu_select)

"""Current hero menu instance."""

def _current_hero_menu_build(menu, index):
    player = Player(index)
    hero = player.hero
    levelinfo = '{hero.level}/{hero.max_level}'.format(hero=hero)
        if not hero.is_max_level() else 'Maxed'

    # Construct menu ready for addition of items
    menu.title = strings.CURRENT_HERO_MENU['Title'].format(
        hero=hero.name,
        levelinfo=levelinfo)
    menu.description = hero.description
    menu.clear()

    for num, skill in enumerate(hero.skills, start=1):
        # Check whether reset should be added
        if num % 6 == 0:
            option = menus.PagedOption(
                strings.CURRENT_HERO_MENU['Reset'].format(gold=cfg.reset_skills_cost),
                None)
            menu.append(option)

        # Append the skill in iteration to the menu
        levelinfo = '{skill.level}/{skill.max_level}'.format(skill=skill)
            if not skill.is_max_level() else 'Maxed'
        option = menus.PagedOption(
            strings.CURRENT_HERO_MENU['Skill'].format(skill=skill.name, levelinfo=levelinfo),
            skill)
        menu.append(option)

def _current_hero_menu_select(menu, index, choice):
    player = Player(index)
    if choice.value is None:
        if player.gold >= cfg.reset_skills_cost:
            for skill in player.hero.skills:
                skill.level = 0
            player.gold -= 50
    else:
        skill = choice.value
        if (skill.cost <= player.hero.skill_points and
                skill.required_level <= player.hero.level and
                not skill.is_max_level()):
            skill.level += 1
    return menu

current_hero_menu = PagedMenu(
    build_callback= _current_hero_menu_build,
    select_callback=_current_hero_menu_select)