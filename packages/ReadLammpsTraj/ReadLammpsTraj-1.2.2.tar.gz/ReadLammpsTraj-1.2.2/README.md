## ReadLammpsTraj
- Read lammps dump trajectory

### Installation

- github:

  ```bash
  git clone https://github.com/eastsheng/ReadLammpsTraj
  cd ReadLammpsTraj
  pip install .
  ```

- pip

  ```
  pip install ReadLammpsTraj
  ```

  

### Usage

```python
import ReadLammpsTraj as RLT

md = RLT.ReadLammpsTraj(f)
# read header info from lammpstrj 
md.__version__()
md.read_info()
# read mass x y z info from lammpstrj 
position = md.read_mxyz(i)
# calculating mass density along z-axis from lammpstrj 
md.oneframe_moldensity(position,Nz=100,id_range=[1,1000],mass_dict={1:15.9994,2:1.00797},id_type="atom",density_type="mass",direction="z")

x,y,z,rho= md.TwoD_Density(position,atomtype_n=[1,2],Nx=60,Ny=1,Nz=60,mass_or_number="mass",id_type="atom")
```



### Fixes

- 1.2.0
  - [x] Many modifications

- 1.1.9
- [x] Add `id_type` arg for `TwoD_Density()` function.
  
- [x] Modify the `read_header()` function

