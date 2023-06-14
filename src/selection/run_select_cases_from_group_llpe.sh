#!/usr/bin/env sh

./select_cases_from_groups.py -i ~/Datasets/SC_50k/common/area_act_chapter_section_info/case_area_act_chapter_section_info.json \
    -s ~/Datasets/IndiaCode/new/CentralActs/section_chapters.json \
    -a ~/Datasets/DHC/raw/area_survey/act_areas.json \
    -o ~/Datasets/LLPE/variations/v1/area_act_chapter_section_info \
    -c "(('Arms Act, 1959_25' in sections) or
        ('Arms Act, 1959_27' in sections) or
        ('Code of Civil Procedure, 1882_115' in sections) or
        ('Code of Civil Procedure, 1882_151' in sections) or
        ('Code of Criminal Procedure, 1973_161' in sections) or
        ('Code of Criminal Procedure, 1973_2' in sections) or
        ('Code of Criminal Procedure, 1973_313' in sections) or
        ('Code of Criminal Procedure, 1973_482' in sections) or
        ('Constitution_1' in sections) or
        ('Constitution_12' in sections) or
        ('Constitution_13' in sections) or
        ('Constitution_132' in sections) or
        ('Constitution_133' in sections) or
        ('Constitution_136' in sections) or
        ('Constitution_14' in sections) or
        ('Constitution_141' in sections) or
        ('Constitution_142' in sections) or
        ('Constitution_15' in sections) or
        ('Constitution_16' in sections) or
        ('Constitution_161' in sections) or
        ('Constitution_162' in sections) or
        ('Constitution_19' in sections) or
        ('Constitution_191' in sections) or
        ('Constitution_2' in sections) or
        ('Constitution_20' in sections) or
        ('Constitution_21' in sections) or
        ('Constitution_22' in sections) or
        ('Constitution_225' in sections) or
        ('Constitution_226' in sections) or
        ('Constitution_227' in sections) or
        ('Constitution_246' in sections) or
        ('Constitution_25' in sections) or
        ('Constitution_3' in sections) or
        ('Constitution_300' in sections) or
        ('Constitution_301' in sections) or
        ('Constitution_309' in sections) or
        ('Constitution_31' in sections) or
        ('Constitution_311' in sections) or
        ('Constitution_32' in sections) or
        ('Constitution_39' in sections) or
        ('Constitution_4' in sections) or
        ('Constitution_5' in sections) or
        ('Constitution_6' in sections) or
        ('Indian Penal Code, 1860_1' in sections) or
        ('Indian Penal Code, 1860_109' in sections) or
        ('Indian Penal Code, 1860_120' in sections) or
        ('Indian Penal Code, 1860_147' in sections) or
        ('Indian Penal Code, 1860_148' in sections) or
        ('Indian Penal Code, 1860_149' in sections) or
        ('Indian Penal Code, 1860_2' in sections) or
        ('Indian Penal Code, 1860_201' in sections) or
        ('Indian Penal Code, 1860_300' in sections) or
        ('Indian Penal Code, 1860_302' in sections) or
        ('Indian Penal Code, 1860_304' in sections) or
        ('Indian Penal Code, 1860_306' in sections) or
        ('Indian Penal Code, 1860_307' in sections) or
        ('Indian Penal Code, 1860_321' in sections) or
        ('Indian Penal Code, 1860_323' in sections) or
        ('Indian Penal Code, 1860_324' in sections) or
        ('Indian Penal Code, 1860_325' in sections) or
        ('Indian Penal Code, 1860_326' in sections) or
        ('Indian Penal Code, 1860_34' in sections) or
        ('Indian Penal Code, 1860_341' in sections) or
        ('Indian Penal Code, 1860_342' in sections) or
        ('Indian Penal Code, 1860_364' in sections) or
        ('Indian Penal Code, 1860_366' in sections) or
        ('Indian Penal Code, 1860_376' in sections) or
        ('Indian Penal Code, 1860_406' in sections) or
        ('Indian Penal Code, 1860_409' in sections) or
        ('Indian Penal Code, 1860_420' in sections) or
        ('Indian Penal Code, 1860_452' in sections) or
        ('Indian Penal Code, 1860_467' in sections) or
        ('Indian Penal Code, 1860_468' in sections) or
        ('Indian Penal Code, 1860_471' in sections) or
        ('Indian Penal Code, 1860_498' in sections) or
        ('Indian Penal Code, 1860_5' in sections) or
        ('Indian Penal Code, 1860_506' in sections) or
        ('Industrial Disputes Act, 1947_25' in sections) or
        ('Negotiable Instruments Act, 1881_138' in sections) or
        ('Special Courts Act, 1979_5' in sections))"
