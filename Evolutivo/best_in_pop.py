# -*- coding: utf-8 -*-
import comparison as cp

def best_individual(pop):
      best = pop[0]
      for ind in pop[1:]:
        best = cp.comparison(best[0], best[1], best[2], ind[0], ind[1], ind[2])

      return best
