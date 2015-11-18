import sys
import logging

def matcher(requirements, candidate):
    logging.info("Matching %s to requirements %s" % (candidate, requirements))
    matched = False
    skillmatch = False
    skillscore = 0
    extraskillscore = 0
    yearscore = 0
    totalscore = 0
    weight = ''

    if set(candidate['skills']):
        if set(requirements['skills']) == set(candidate['skills']):
            skillscore += 2
            skillmatch = True
        else:
            if set(requirements['skills']).issuperset(set(candidate['skills'])):
                skillscore += 1
                skillmatch = True
            elif set(requirements['skills']).issubset(set(candidate['skills'])):
                skillscore += 3
                skillmatch = True
            elif bool(set(requirements['skills']).intersection(set(candidate['skills']))):
                skillscore += 1
                skillmatch = True

    optionalskills = set(requirements['optional'])
    extraskills = set(candidate['skills']) - set(requirements['skills'])

    if extraskills and optionalskills:
        if set(optionalskills) == set(extraskills):
            extraskillscore += 0.5
            skillmatch = True
        else:
            if set(optionalskills).issuperset(set(extraskills)):
                extraskillscore += 0.25
            elif set(optionalskills).issubset(set(extraskills)):
                extraskillscore += 0.75
            elif bool(set(optionalskills).intersection(set(extraskills))):
                extraskillscore += 0.25

    if skillmatch:
        matched = True
        if requirements['years'] == candidate['years']:
            yearscore += 1
        elif requirements['years'] < candidate['years']:
            yearscore += 1
            diff = candidate['years'] - requirements['years']
            yearscore += diff / float(2)

        if skillscore == 2 and yearscore == 1:
            weight = 'exact'
        elif skillscore == 2 and yearscore > 1:
            weight = 'strong'
        elif skillscore > 2 and yearscore == 1:
            weight = 'strong'
        elif skillscore > 2 and yearscore > 1:
            weight = 'strong'
        elif skillscore == 2 and yearscore < 1:
            weight = 'weak'
        elif skillscore < 2 and yearscore == 1:
            weight = 'weak'
        elif skillscore < 2 and yearscore < 1:
            weight = 'weak'
        elif skillscore > 2 and yearscore < 1:
            weight = 'weak'
        elif skillscore < 2 and yearscore > 1:
            weight = 'weak'

    totalscore = skillscore + yearscore + extraskillscore

    logging.info("Got match {}, score: {},  weight: {} for candidate {}".format(matched,
                                                                         totalscore,
                                                                         weight,
                                                                         candidate['name']))
    logging.info("---------------------------------------------------------------------------------------------------------------------")
    return matched, totalscore, weight


if __name__ == '__main__':
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    root.addHandler(ch)
    
    requirements = {'years': 2,
                    'skills': ['Python', 'Ruby', 'Rust', 'Erlang', 'Elixir'],
                    'optional': ['C', 'C++']}

    candidate1 = {'name': 'Candidate1', 'years': 3,
                  'skills': ['Python', 'Ruby', 'Rust', 'Erlang', 'Elixir']}

    candidate2 = {'name': 'Candidate2', 'years': 3,
                  'skills': ['Python', 'Ruby', 'Rust', 'Erlang', 'Elixir', 'C']}

    candidate3 = {'name': 'Candidate3', 'years': 3,
                  'skills':  ['Python', 'Ruby', 'C++', 'C']}

    candidate4 = {'name': 'Candidate4', 'years': 3,
                  'skills': ['ASP.NET', 'C#', 'Delphi', 'PHP', 'C++']}

    matcher(requirements, candidate1)
    matcher(requirements, candidate2)
    matcher(requirements, candidate3)
    matcher(requirements, candidate4)
