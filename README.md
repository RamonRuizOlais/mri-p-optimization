# Optimization of Multi-modal Relaxometry MR Acquisitions for Estimating Quantitative Brain Microstructure Parameters

Authors:
- Ashley Aguilar-Salinas¹ (ashaguilar06@gmail.com)
- Alonso Ramírez-Manzanares² (alram@cimat.mx)
- Ramon Ruiz-Olais² (ramon.ruiz@cimat.mx)
- Carlos Segura² (carlos.segura@cimat.mx)

¹ Escuela Nacional de Estudios Superiores UNAM (ENES Morelia), Mexico  
² Computer Science Department, Centro de Investigación en Matemáticas, A.C.

---

## Abstract

This project addresses the automatic optimization of magnetic resonance imaging (MRI) acquisition protocols to improve the estimation of brain microstructure descriptors, with a focus on myelin fraction. The problem is formulated as a binary optimization task with constraints, where each decision variable encodes whether a specific repetition time is included in the protocol.

Different approximated optimization strategies are analyzed, including:
- Local search
- Memetic algorithms with and without explicit diversity control

The results show that population-based strategies significantly outperform both local search and fixed reference protocols, reducing the relative estimation error by over 30%.

**Keywords:** Magnetic Resonance Imaging, Acquisition Protocol Optimization, Myelin Fraction Estimation, Memetic Algorithms, Combinatorial Optimization.

---

## Introduction

Problem Context

Magnetic Resonance Imaging (MRI) is a fundamental non-invasive neuroimaging technique for:
- Generating high-resolution anatomical and functional images
- Characterizing physical properties of biological tissues
- Studying the structure of the central nervous system

Currently, key acquisition parameters (Repetition Time (TR) and Echo Time (TE)) are typically configured with default values provided by the equipment, based on empirical knowledge and technological limitations.

Research Opportunity

There is an opportunity to refine acquisition protocols from a computational and systematic perspective, using:
- Combinatorial optimization techniques
- Physiologically realistic simulations
- Experimental constraints

Objectives

1. Automatically optimize MRI acquisition configurations
2. Minimize the estimation error of myelin fraction
3. Compare optimization strategies (local search vs. memetic algorithms)
4. Validate results under realistic conditions

---

## Problem Formulation

MRI Fundamentals

MRI is based on the behavior of hydrogen protons when subjected to a strong magnetic field:

- TR (Repetition Time): Interval between successive excitation pulses
- TE (Echo Time): Time between pulse application and signal acquisition
- T1: Longitudinal relaxation time (realignment with the field)
- T2: Transverse relaxation time (loss of phase coherence)

Three-Compartment Model

The MR signal is modeled as a convex combination of three tissue compartments:

1. Myelin (m)
2. Intra/Extracellular (ie)
3. Cerebrospinal Fluid (CSF)

Each compartment has:
- Specific T1 and T2 values
- A relative fraction within the voxel

Computational Representation

Each protocol P is represented as a binary vector $\mathbf{x} = [x_1, x_2, ..., x_n]$ where:
- $x_i = 1$ if TR$_i$ is selected
- $x_i = 0$ otherwise

Constraints:
- Total sum of TR ≤ predefined threshold (maximum protocol duration)
- Feasible solution space limited by technical and medical constraints

---

## Methodology

1. Computational Cost Reduction Strategy

A procedure was implemented to determine the optimal number of voxels:

- 200 random protocols were evaluated using 200 voxels as reference
- Subsets of different sizes (1-50 voxels) were tested
- Ranking distance with respect to reference was measured

Result: From 40 voxels onward, the distance tends to stabilize, allowing significant reduction in computational time without compromising fidelity.

2. Objective Function

For a protocol P and N_v voxels:

$$f(P) = \frac{1}{N_v} \sum_{i=1}^{N_v} |f_m^{est}(i) - f_m^{ref}(i)|$$

Where:
- $f_m^{est}(i)$ = Estimated myelin fraction at voxel $i$
- $f_m^{ref}(i)$ = Reference myelin fraction at voxel $i$

Evaluation procedure:
1. Generate synthetic signals with random tissue fractions
2. Simulate MR signal using biophysical model
3. Add Rician noise (realistic SNR)
4. Re-estimate parameters via curve fitting
5. Calculate estimation error

3. Optimization Algorithms

A. Local Search (Algorithm 2)

Operator: Binary flip (single bit change)

Procedure:
1. Generate random binary solution
2. Explore neighborhood (configurations differing by one bit)
3. Accept improvements reducing error more than threshold $\epsilon$
4. In case of tie, prefer protocol with lower TR sum
5. Repeat until convergence

Advantages: Computationally efficient  
Disadvantages: Susceptible to local optima

B. Memetic Algorithms (Algorithms 3 and 4)

Combine:
- Global exploration through classical evolutionary mechanisms
- Local exploitation through iterative local search

Implemented variants:

MA-GenElit (without diversity control):
- Binary tournament selection
- Two-point crossover
- Generational replacement with elitism

MA-BNP (with diversity control - Best Non-Penalized):
- Same structure as MA-GenElit
- BNP strategy in survivor selection
- Considers similarity between solutions

Customized distance metric:

$$d(P_i, P_j) = \frac{1}{|TR_i| + |TR_j|} \left( \sum_{tr \in TR_i} \min_{tr' \in TR_j} |tr - tr'| + \sum_{tr \in TR_j} \min_{tr' \in TR_i} |tr - tr'| \right)$$

This metric captures actual overlap among selected TR values.

Parameters:
- Population size: 30 individuals
- Generations: 100
- Stopping criterion: fixed number of generations

---

## Results

Experimental Configuration

Baseline conditions established:
- SNR: 100 (recommended by experts)
- Voxels for evaluation: 40 (time optimization)
- Voxels for validation: 400 (realistic scenarios)

4.2 Local Search Analysis

100 independent executions:
- Wide dispersion of results (relative error: 0 to 0.6+)
- Some acceptable protocols, but inconsistent
- Tendency to get trapped in local optima

Conclusion: Local search does not guarantee necessary robustness.

4.3 Memetic Algorithms

Comparison MA-GenElit vs MA-BNP:

| Metric | MA-GenElit | MA-BNP |
|--------|-----------|---------|
| Mean relative error | 0.04-0.05 | 0.04-0.05 |
| Error range | Narrower | Similar |
| Diversity | Lower | Higher |
| Convergence | Stable | Stable |

Findings: Both variants show similar performance. With only 100 generations, explicit diversity does not provide substantial improvement (consistent with literature: benefits more apparent in longer runs).

4.4 Global Comparison

```
Performance ranking (by relative estimation error):

1. MA-BNP and MA-GenElit      ≈ 0.04-0.05 
2. Empirical protocol (Ref)    ≈ 0.09     
3. Reference protocol          ≈ 0.10    
4. Local search (variable)     0.04-0.6+ 
```

Memetic algorithms achieve consistent error rates of 0.04-0.05, reducing estimation error by approximately 55% compared to reference protocols. Local search shows high variability (0.04 to 0.6+) and cannot guarantee reliable solutions, while population-based methods provide stable, superior performance. BNP diversity control maintains higher solution diversity without compromising final quality, suggesting potential benefits in longer optimization runs.


4.5 Optimized Protocol Validation

Selected protocol: MA-BNP variant (best overall performance)

Validation conditions:
- SNR: 100
- Voxels: 400
- TE: Kept fixed

Comparative results:

| Parameter | Ref Protocol | Emp Protocol | Opt Protocol | Improvement |
|-----------|-------------|--------------|-------------|-------------|
| Myelin Fraction ($f_m$) | 0.10 | 0.09 | 0.0675 | 30%↓ |
| Voxels with error <10% | 233/400 | 304/400 | 326/400 | +93 |
| $f_{ie}$ (intra/extra water) | 0.06 | 0.02 | 0.0255 | Better |
| CSF ($f_{csf}$) | 1.26 | 0.21 | 0.6646 | Better |

Robustness: The protocol maintains good performance even with 40 voxels (≠ 400).

---

## Repository Structure

```
mri-p-optimization/
├── main.py                    # Main optimization
├── main_vox.py               # Variant with voxel evaluation
├── objective_function.py      # Objective function (error calculation)
├── calculate_error.py         # Error calculation functions
├── error.py                   # Error module
├── feasible.py               # Feasible solution checking
├── random_solution.py        # Random solution generation
├── ordenar_solucion.py       # Sorting utilities
├── gen_functions.py          # General functions
├── mide_tiempo.py            # Execution time measurement
├── trajectory.py             # Trajectory analysis
├── conversion_TR.py          # TR parameter conversion
│
├── Evolutivo/                # Evolutionary algorithms
│   ├── main.py              # Main evolutionary entry point
│   ├── main_bnp.py          # Memetic algorithm with BNP
│   ├── main_results.py      # Results analysis
│   ├── local_search.py      # Local search implementation
│   ├── poblacional.py       # Base population algorithm
│   ├── poblacional_BNP.py   # Population algorithm with BNP
│   ├── crossover_two_points.py  # Crossover operator
│   ├── selection.py         # Selection strategies
│   ├── BNP.py              # BNP strategy
│   ├── best_in_pop.py      # Best individual in population
│   └── ...
│
├── README.md                 # This file
└── slurm_script_*           # Scripts for cluster execution
```

---

## Requirements and Dependencies

Python >= 3.8

Main libraries:
```
numpy              # Numerical computation
scipy              # Optimization and curve fitting
matplotlib         # Visualization
pandas             # Data analysis
```

Installation:
```bash
pip install numpy scipy matplotlib pandas
```

---

## Usage

Run Local Optimization

```bash
python main.py
```

Run Memetic Algorithm

```bash
python Evolutivo/main_bnp.py
```

Analyze Results

```bash
python Evolutivo/main_results.py
```

On SLURM Cluster

```bash
sbatch slurm_script_Projects_Type1.sh
```

---

## Parameter Configuration

Edit the following values in main scripts:

```python
# MRI parameters
SNR = 100                      # Signal-to-noise ratio
NUM_VOXELS = 40               # Voxels for evaluation
MAX_ACQUISITION_TIME = 5000   # ms (maximum allowed)

# Optimization parameters
POPULATION_SIZE = 30           # Individuals
NUM_GENERATIONS = 100          # Generations
EPSILON = 0.01                 # Improvement threshold for local search

# TR (Repetition Time) range
TR_MIN = 100                   # ms
TR_MAX = 3000                  # ms
TR_STEP = 100                  # ms
```

---

## Key Findings

Main Conclusions

1. Systematic optimization is viable: Optimization algorithms can design MRI protocols superior to empirical configurations.

2. Superiority of population-based algorithms: Memetic algorithms consistently outperform local search, reducing error >30%.

3. Computational robustness: The optimized protocol maintains excellent performance even with reduced evaluations (40 voxels).

4. Diversity control: While BNP showed no drastic improvement in 100 generations, it does not impair performance and can be beneficial in more intensive searches.

5. Multiple benefits: Optimization improves not only myelin estimation but also other tissue parameters (CSF, T1, T2, flip-angle).

---

## Future Directions

Immediate Improvements

- [ ] Optimize also echo times (TE)
- [ ] Multi-objective formulations if errors are uncorrelated
- [ ] Adapt strategies to other body regions

Computational Challenges

- Cost of realistic simulations is the main bottleneck
- Promising solution: Train predictive neural networks to estimate errors without running full simulation

Clinical Applications

- Multiple sclerosis diagnosis
- Early detection of neurodegenerative diseases
- Patient-specific optimization

---

## References

    1. Adria, G., Attivissimo, F., Cavone, G., & Lanzolla, A. M. L. (2009). Acquisition times in magnetic resonance imaging: Optimization in clinical use. IEEE Transactions on Instrumentation and Measurement, 58(9), 3140–3148. https://doi.org/10.1109/TIM.2009.2016888
    2. Alancay, N., Villagra, S., & Villagra, A. (2016). Algoritmos metaheurísticos trayectoriales para optimizar problemas combinatorios. Informes Científicos Técnicos - UNPA, 8(3), 56–75. https://doi.org/10.22305/ict-unpa.v8i3.222
    3. Alancay, N., Villagra, S., & Villagra, A. (2016). Metaheurísticas de trayectoria y poblacional aplicadas a problemas de optimización combinatoria. Informes Científicos Técnicos - UNPA, 8(1), 202–220. https://doi.org/10.22305/ict-unpa.v8i1.157
    4. Angeline, P.J., & Kinnear, K.E. (Eds.) (1996). Advances in Genetic Programming. (vol. 2). MIT Press. 
    5. Bandala Álvarez, D., & Pérez González, J. (2023). Estimación del mapa de anisotropía fraccional y difusividad media en materia blanca utilizando transformers. Research in Computing Science, 152(8), 209-220.
    6. Bao, Z., & Watanabe, T. (2009). A novel genetic algorithm with cell crossover for circuit design optimization. 2009 IEEE International Symposium on Circuits and Systems, (pp. 2982–2985). https://doi.org/10.1109/ISCAS.2009.5118429
    7. Bäck, T., Hammel, U., & Schwefel, H.-P. (1997). Evolutionary Computation: Comments on the History and Current State. IEEE Transactions on Evolutionary Computation, 1(1), 3-17. https://doi.org/10.1109/4235.585888
    8. Beretta, R., Cotta, C., & Moscato, P. (2003), Enhancing the performance of memetic algorithms by using a matching-based recombination algorithm. In M. Resende & J. Pinho de Sousa (Eds.), Metaheuristics: Computer-Decision Making (vol 86, pp. 65-90) https://doi.org/10.1007/978-1-4757-4137-7_4
    9. Braskie, M. N., & Thompson, P. M. (2014). A focus on structural brain imaging in the Alzheimer's disease neuroimaging initiative. Biological psychiatry, 75(7), 527–533. https://doi.org/10.1016/j.biopsych.2013.11.020
    10. Buxton, R.B. (2009). Introduction to functional magnetic resonance imaging: Principles and techniques (2nd ed.) Cambridge University Press
    11. Caballero, J. A., & Grossmann, I. E. (2007). Una revisión del estado del arte en optimización. Revista Iberoamericana de Automática e Informática Industrial, 4(1), 5-23
    12. Cabrera Hipólito, S. E. (n.d.). Resonancia magnética: Bases físicas y aplicaciones clínicas del tensor de difusión y la tractografía. Interciencia, 28(1), 28–31. https://interciencia.org
    13. Canales-Rodríguez, E. J., Pizzolato, M., Piredda, G. F., Hilbert, T., Kunz, N., Pot, C., Yu, T., Salvador, R., Pomarol-Clotet, E., Kober, T., Thiran, J.-P., & Daducci, A. (2021). Comparison of non-parametric T2 relaxometry methods for myelin water quantification. Medical Image Analysis. Medical Image Analysis, 69. https://doi.org/10.1016/j.media.2021.101959
    14. Capilla, A. (n.d.), Evolución de las técnicas de neuroimagen [Poster presentation]. PSI Expo, Universidad Autónoma de Madrid. https://www.uam.es/uam/media/doc/1606888904010/psi-expo-avances-posters-evolucion.pdf
    15. Cárdenes Almeida, R., Muñoz Moreno, E., Tristán Vega, A., & Martín Fernández, M. (2008).  Una herramienta para el procesado y visualización de imágenes de resonancia magnética de tensor de difusión [Conference presentation]. 26th  Annual Congress of the Spanish Society of Biomedical Engineering, Valladolid, Spain.
    16. Clínica Universidad de Navarra. (n.d.). Neuroimagen. Retrieved July 9, 2025, from https://www.cun.es/diccionario-medico/terminos/neuroimagen
    17. CogniFit. (n.d.). ¿Qué es el cerebro humano?. Retrieved July 10, 2025, from  https://www.cognifit.com/co/cerebro
    18. Conversano, F., Greco, A., Casciaro, E., Ragusa, A., Lay-Ekuakille, A., & Casciaro, S. (2012).  Imágenes ultrasónicas armónicas de agentes de contraste de tamaño nanométrico para diagnósticos moleculares multimodales. IEEE Transactions on Instrumentation and Measurement, 61(7), 1848-1856.
    19. Corbetta, M., & Shulman, G. L. (2002). Control of goal-directed and stimulus-driven attention in the brain. Nature reviews. Neuroscience, 3(3), 201–215. https://doi.org/10.1038/nrn755
    20. Eiben, A. E., & Smith, J. E. (2003). Introduction to evolutionary computing. Springer. https://doi.org/10.1007/978-3-662-05094-1
    21. Escorza Aguilar, A. M. (2016). Protocolo para analizar Diffusion Tensor Imaging (DTI) del cerebro humano (Undergraduate thesis, Universidad de Sevilla, Spain).
    22. Fuster, J. M. (2015). Cerebro y mente: Una visión desde la neurociencia. Revista de neurología, 61(11), 469-480. https://doi.org/10.33588/rn.6111.2015172
    23. Gonzalo, R., & Falcón, C. (2014). Control de calidad en imagen por resonancia magnética: Evaluación de parámetros de calidad en protocolos de neuroimagen. Revista Chilena de Radiología, 21, 10-17. https://doi.org/10.4067/S0717-93082015000100004
    24. Hernández, J. A., Dorado, J., Gestal, M., & Porto, A. B. (2007). Avances en algoritmos evolutivos, En C. Dafonte, Á. Gómez, & F. J. Penousal (Eds.).  Inteligencia artificial y computación avanzada (pp.35-53). Fundación Alfredo Brañas.
    25. Holland, J.H. (1992). Adaptation in Natural and Artificial Systems: An Introductory Analysis with Applications to Biology, Control, and Artificial Intelligence. MIT Press. 
    26. Jack, C. R., Jr, Barnes, J., Bernstein, M. A., Borowski, B. J., Brewer, J., Clegg, S., Dale, A. M., Carmichael, O., Ching, C., DeCarli, C., Desikan, R. S., Fennema-Notestine, C., Fjell, A. M., Fletcher, E., Fox, N. C., Gunter, J., Gutman, B. A., Holland, D., Hua, X., Insel, P., … Weiner, M. (2015). Magnetic resonance imaging in Alzheimer 's Disease Neuroimaging Initiative 2. Alzheimer's & dementia : the journal of the Alzheimer's Association, 11(7), 740–756. https://doi.org/10.1016/j.jalz.2015.05.002
    27. Jenkinson, M., & Chappell, M. (2018). Introduction to Neuroimaging Analysis. Oxford University Press.
    28. Jiménez Lozano, G. (2009). Optimización. Universidad Nacional de Colombia, Sede Manizales.
    29. Lugo, L., Segura, C., & Miranda, G. (2022). A diversity-aware memetic algorithm for the linear ordering problem. Memetic Computing, 14(3), 395-409. https://doi.org/10.1007/s12293-022-00378-5
    30. Manes, F. (2014). Usar el cerebro (4a ed.) Planeta.
    31. Martí, R. (2003). Procedimientos metaheurısticos en optimización combinatoria. Matemátiques, Universidad de Valencia, 1(1), 3-62.
    32. Moscato, P., & Cotta, C. (2003). A gentle introduction to memetic algorithms. In F. Glover, & G. Kochenberger (Eds.), Handbook of metaheuristics (Vol. 57, pp. 105-144). Springer. https://doi.org/10.1007/0-306-48056-5_5
    33. National Institute of Neurological Disorders and Stroke. (n.d.). Brain basics: Know your brain. Retrieved July 10, 2025, from https://www.ninds.nih.gov/health-information/public-education/brain-basics/brain-basics-know-your-brain
    34. Norman, M., & Moscato, P. (1989). A Competitive-Cooperative Approach to Complex Combinatorial Search. (Technical Report No. 790). California Institute of Technology, Concurrent Computation Program.
    35. Osman, I.H. and Kelly, J.P. (Eds.) (1996). Meta-Heuristics: Theory and Applications. Kluwer Academic.  https://doi.org/10.1007/978-1-4613-1361-8
    36. Rojas, G., Cordovez, J., Gálvez, M., Cisternas, J., Asahi, T., & Bravo, E. (2007). Uso combinado de resonancia magnética funcional (fMRI) y tractografía para seleccionar tractos específicos de sustancia blanca: Experiencia preliminar. Revista chilena de Radiología, 14, 227-230. https://doi.org/10.4067/S0717-93082008000400007
    37. Rueda, A. del P., & Enríquez, L. F. (2018). Una revisión de técnicas básicas de neuroimagen para el diagnóstico de enfermedades neurodegenerativas. Revista Biosalud, 17(2), 59–90. https://doi.org/10.17151/biosa.2018.17.2.5
    38. Schiavinotto, T., Stützle, T. (2004). The linear ordering problem: instances, search space analysis and algorithms. Journal of Mathematical Modelling and Algorithms, 3(4), 367–402 https://doi.org/10.1023/B:JMMA.0000049426.06305.d8
    39. Tang, J., Lim, M.H. & Ong, Y.S. (2007). Diversity-adaptive parallel memetic algorithm for solving large scale combinatorial optimization problems. Soft Comput 11, 873–888. https://doi.org/10.1007/s00500-006-0139-6
    40. Tritrakarn, T., Takahashi, M., & Okamura, T. (2024). Optimization of RF coil geometry for NMR/MRI applications using a genetic algorithm. Journal of magnetic resonance, 362, 107685. https://doi.org/10.1016/j.jmr.2024.107685
    41. Universidad Veracruzana. (n.d.). El cerebro en el  tiempo Recorrido de la Neurociencia. Retrieved July 8, 2025, from https://www.uv.mx/cienciauv/blog/cerebroeneltiemponeurociencia/
    42. Wright, G. A., Hu, B. S., & Macovski, A. (1991). Estimating oxygen saturation of blood in vivo with MR imaging at 1.5 T. Magnetic resonance imaging, 14, 275–283. https://doi.org/10.1002/jmri.1880010303
    43. Wright, G. A., Nishimura, D. G., & Macovski, A. (1991). Flow-independent magnetic resonance projection angiography. Magnetic resonance in medicine, 17(1), 126–140. https://doi.org/10.1002/mrm.1910170117


---
