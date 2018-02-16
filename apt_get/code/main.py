import sys
# # sys.path.append('/Users/Reed/PycharmProjects/akara/apt_get/code')
sys.path.insert(0, '.code/foo')
from foo import hoodtodf
from foo import cleaning
from foo import analysis

# GB_Hood = ['https://www.apartments.com/pike-place-market-seattle-wa/']
# Cleveland_Hood = ['https://www.apartments.com/downtown-cleveland-cleveland-oh/']
# Miami_Hood = ['https://www.apartments.com/wynwood-miami-fl/']
# Denver_Hood = ['https://www.apartments.com/five-points-denver-co/']
# Phoenix_Hood = ['https://www.apartments.com/downtown-phoenix-phoenix-az/']

hood_choices = ['https://www.apartments.com/southwest-dc-washington-dc/']
paths_unclean = hoodtodf.main(hood_choices)
paths_clean = cleaning.main(paths_unclean)
analysis.main(paths_clean)











