
class DoubleWell():

    """Particles in an double well potential

    Test system with particles in a quadratic double well potential.

    Attributes
    ----------
    system
        Openmm system
    potential_expression
        External potential expression as a sympy function.
    potential_parameters
        Dictionary with the values of the parameters of the potential.

    """


    system = None
    potential_expression = None
    potential_parameters = None

    def __init__(self, n_particles, mass, Eo, a, b):

        """Creating a new instance of DoubleWell

        A new test system is returned with the openmm system of particles in an external double
        well potential:

             $Eo*((\frac{x}{a})**4-2.0*(\frac{x}{a})**2)-\frac{b}{a}*x + 0.5*\frac{8.0*Eo}{a^{2}}*(y^2 + z^2)$

        Parameters
        ----------

        n_particles: int
            Number of particles in the system
        mass: unit.Quantity
            Mass of the particles
        Eo: unit.Quantity
            Parameter of the external potential with units of energy.
        a: unit.Quantity
            Parameter of the external potential with units of length.
        b: unit.Quantity
            Parameter of the external potential with units of energy.

        Examples
        --------

        >>> from uibcdf_test_systems import DoubleWell
        >>> from simtk import unit
        >>> double_well_potential = DoubleWell(n_particles = 1, mass = 64 * unit.amu, Eo=4.0 * unit.kilocalories_per_mole, a=1.0 * unit.nanometers, b=0.0 * unit.kilocalories_per_mole))

        Notes
        -----

        See `corresponding documentation in the user guide regarding this class
        <../../systems/free_particle.html>`_.

        """

        # OpenMM system

        import simtk.openmm as mm
        import simtk.unit as unit
        import simtk.openmm.app as app

        self.system = mm.System()

        for ii in range(n_particles):
            self.system.addParticle(mass)

        k = 8.0*Eo/(a**2) # stiffness of the armonic potential for coordinates Y and Z

        A = Eo/(a**4)
        B = -2.0*Eo/(a**2)
        C = -b/a
        D = k/2.0

        force = mm.CustomExternalForce('A*x^4+B*x^2+C*x + D*(y^2+z^2)')
        force.addGlobalParameter('A', A)
        force.addGlobalParameter('B', B)
        force.addGlobalParameter('C', C)
        force.addGlobalParameter('D', D)

        for ii in range(n_particles):
            force.addParticle(ii, [])
        self.system.addForce(force)

        # Potential expresion and constants

        from sympy import symbols

        self.potential_parameters ={'Eo':Eo, 'a':a, 'b':b}

        x, y, z, Eo, a, b = symbols('x y z Eo a b')
        self.potential_expression = Eo*((x/a)**4-2.0*(x/a)**2)-(b/a)*x + 0.5 *(8.0*Eo/a**2)*(y**2 + z**2)
        del(x, y, z, Eo, a, b)

    def potential(self, coordinates):

        from numpy import array

        coordinates._value = array(coordinates._value)
        Eo = self.potential_parameters['Eo']
        a = self.potential_parameters['a']
        b = self.potential_parameters['b']

        if len(coordinates._value.shape)==1 and coordinates._value.shape[0]==3:

            x  = coordinates[0]
            y  = coordinates[1]
            z  = coordinates[2]

            return Eo*((x/a)**4-2.0*(x/a)**2)-(b/a)*x + 0.5 *(8.0*Eo/a**2)*(y**2 + z**2)

        elif len(coordinates._value.shape)==2 and coordinates._value.shape[1]==3:

            x  = coordinates[:,0]
            y  = coordinates[:,1]
            z  = coordinates[:,2]

            return Eo*((x/a)**4-2.0*(x/a)**2)-(b/a)*x + 0.5 *(8.0*Eo/a**2)*(y**2 + z**2)

        else:

            raise ValueError('The input argument coordinates needs a specific shape.')

