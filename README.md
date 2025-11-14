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

[43 complete references from the original research article]

---

## Publication

Article: Optimization of Multi-modal Relaxometry MR Acquisitions for Estimating Quantitative Brain Microstructure Parameters

Received: Dec 26, 2016  
Accepted: Dec 11, 2017

---

## License

[Specify license if applicable]

---

## Contact

For inquiries about this project, contact:
- Ashley Aguilar-Salinas: ashaguilar06@gmail.com
- Alonso Ramírez-Manzanares: alram@cimat.mx

---

Last Updated: November 13, 2025
