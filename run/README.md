## Useful links
- https://curiosityfluids.com/2016/04/01/pressure-driven-nozzle-flow-with-shock-rhocentralfoam/
- https://curiosityfluids.com/2016/07/14/converging-diverging-nozzle-v2-rhocentralfoam/

## What works

The settings described here: https://curiosityfluids.com/2016/07/14/converging-diverging-nozzle-v2-rhocentralfoam/.

### Initial condition

Setup a shock tube type IC with stagnation conditions on left and exit conditions on right. Give zero velocity everywhere.

### Boundary conditions

- Inflow
    - p: `totalPressure`
    - T: `totalTemperature`
    - U: `zeroGradient`
- Outflow
    - p, T, U: `zeroGradient`
- Wall
    - p, T: `zeroGradient`
    - U: `slip`

Lateral sides have wedge BC.

## Conical vs Rao nozzle

The parameters given in [../Bell_nozzle_design_methodology.pdf](../Bell_nozzle_design_methodology.pdf) and slide 20 of [../../Rocket_Performance_Parameters_Nozzles.pdf](../../Rocket_Performance_Parameters_Nozzles.pdf) are different. Using the latter ones.