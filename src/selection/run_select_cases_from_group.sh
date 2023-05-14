#!/usr/bin/env sh

./select_cases_from_groups.py -i ~/Datasets/SC_50k/variations/var_2/area_act_chapter_section_info/overall/case_area_act_chapter_section_info.json \
    -s ~/Datasets/IndiaCode/new/CentralActs/section_chapters.json \
    -a ~/Datasets/DHC/variations/var_1/surveys/areas/Mitali/act_to_area_mapping.json \
    -o ~/Datasets/SC_50k/variations/var_2/area_act_chapter_section_info/with_selected_areas \
    -c "(('CRIMINAL LAW' in areas) or
        ('CONSTITUTIONAL LAW' in areas) or
        ('CIVIL LAW' in areas) or
        ('JUDICIARY AND COURTS LAW' in areas) or
        ('PROPERTY LAW' in areas) or
        ('NATIONAL SECURITY LAW' in areas) or
        ('INTELLECTUAL PROPERTY LAW' in areas) or
        ('CONTRACT LAW' in areas) or
        ('COMPANY OR BUSINESS OR CORPORATE LAW' in areas) or
        ('TRANSPORTATION LAW' in areas) or
        ('BANKING AND FINANCE LAW' in areas) or
        ('TAX LAW' in areas) or
        ('FAMILY LAW' in areas) or
        ('GOVERNMENT LAW' in areas) or
        ('HUMAN RIGHTS LAW' in areas) or
        ('ELECTION LAW' in areas) or
        ('ADMINISTRATIVE LAW' in areas) or
        ('INTERPRETATION OF STATUTES' in areas) or
        ('EDUCATION LAW' in areas) or
        ('INTERNATIONAL LAW' in areas) or
        ('MOTOR VEHICLES LAW' in areas) or
        ('MEDICAL AND HEALTHCARE LAW' in areas) or
        ('TRADE LAW' in areas) or
        ('IMMIGRATION LAW' in areas) or
        ('ENERGY LAW' in areas) or
        ('TELECOMMUNICATION LAW' in areas) or
        ('RTI LAW' in areas) or
        ('CYBER LAW' in areas) or
        ('INSURANCE LAW' in areas) or
        ('COMPETITION LAW' in areas) or
        ('ENVIRONMENT LAW' in areas) or
        ('MEDIA LAW' in areas) or
        ('CONSUMER LAW' in areas) or
        ('ESTATE PLANNING (WILLS AND TRUSTS) LAW' in areas) or
        ('AGRICULTURE LAW' in areas) or
        ('AVIATION LAW' in areas))"
