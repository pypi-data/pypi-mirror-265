from ..types import Vector, CartesianState, KeplerianState
from .core import PlotSetup, MultiPlot, Base3D

# TODO: FIX OVERRIDE ISSUE IN PLOT METHODS


class PlotKeplerianState(MultiPlot):
    """Plot evolution of classical keplerian elements"""

    def __init__(self, setup: PlotSetup = PlotSetup()) -> None:

        if setup.xlabel is None:
            _xlabel = "Days past initial epoch"
        else:
            _xlabel = setup.xlabel

        setup.subplots = (3, 2)

        base_setup = PlotSetup(xlabel=_xlabel, grid=setup.grid, legend=setup.legend)

        self.a_setup = base_setup.copy()
        self.a_setup.ylabel = "$a$ [km]"

        self.e_setup = base_setup.copy()
        self.e_setup.ylabel = "$e$"

        self.i_setup = base_setup.copy()
        self.i_setup.ylabel = "$i$ [deg]"

        self.omega_setup = base_setup.copy()
        self.omega_setup.ylabel = "AoP [deg]"

        self.Omega_setup = base_setup.copy()
        self.Omega_setup.ylabel = "RAAN [deg]"

        self.nu_setup = base_setup.copy()
        self.nu_setup.ylabel = "TA [deg]"

        super().__init__(setup)

        # Initialize subplots
        self.a_subplot = self.add_plot(self.a_setup)
        self.e_subplot = self.add_plot(self.e_setup)
        self.i_subplot = self.add_plot(self.i_setup)
        self.omega_subplot = self.add_plot(self.omega_setup)
        self.Omega_subplot = self.add_plot(self.Omega_setup)
        self.nu_subplot = self.add_plot(self.nu_setup)

        return None

    def add_line(
        self, time: Vector, state: KeplerianState, label: str | None = None
    ) -> None:

        dt = (time - time[0]) / (24.0 * 3600.0)

        self.a_subplot.add_line(dt, state.a * 1e-3, label=label)
        self.e_subplot.add_line(dt, state.e, label=label)
        self.i_subplot.add_line(dt, state.i, label=label)
        self.omega_subplot.add_line(dt, state.omega, label=label)
        self.Omega_subplot.add_line(dt, state.Omega, label=label)
        self.nu_subplot.add_line(dt, state.nu, label=label)

        return None

    def plot(self, time: Vector, state: KeplerianState) -> str:
        """Plot evolution of classical keplerian elements

        :param time: Time vector [s]
        :param state: Keplerian state
        """

        self.add_line(time, state)

        return self.__call__()

    def __call__(self) -> str:

        self.a_subplot()
        self.e_subplot()
        self.i_subplot()
        self.omega_subplot()
        self.Omega_subplot()
        self.nu_subplot()

        return super().__call__()


class PlotCartesianState(MultiPlot):

    def __init__(self, setup: PlotSetup = PlotSetup()) -> None:

        if setup.xlabel is None:
            _xlabel = "Days past initial epoch"
        else:
            _xlabel = setup.xlabel

        setup.subplots = (3, 2)

        base_setup = PlotSetup(xlabel=_xlabel, grid=setup.grid, legend=setup.legend)

        self.x_setup = base_setup.copy()
        self.x_setup.ylabel = "$x$ [km]"

        self.y_setup = base_setup.copy()
        self.y_setup.ylabel = "$y$ [km]"

        self.z_setup = base_setup.copy()
        self.z_setup.ylabel = "$z$ [km]"

        self.vx_setup = base_setup.copy()
        self.vx_setup.ylabel = "$v_x$ [km/s]"

        self.vy_setup = base_setup.copy()
        self.vy_setup.ylabel = "$v_y$ [km/s]"

        self.vz_setup = base_setup.copy()
        self.vz_setup.ylabel = "$v_z$ [km/s]"

        super().__init__(setup)

        # Generate subplots
        self.x_subplot = self.add_plot(self.x_setup)
        self.y_subplot = self.add_plot(self.y_setup)
        self.z_subplot = self.add_plot(self.z_setup)
        self.vx_subplot = self.add_plot(self.vx_setup)
        self.vy_subplot = self.add_plot(self.vy_setup)
        self.vz_subplot = self.add_plot(self.vz_setup)

        return None

    def add_line(
        self, time: Vector, state: CartesianState, label: str | None = None
    ) -> None:

        dt = (time - time[0]) / (24.0 * 3600.0)

        self.x_subplot.add_line(dt, state.x * 1e-3, label=label)
        self.y_subplot.add_line(dt, state.y * 1e-3, label=label)
        self.z_subplot.add_line(dt, state.z * 1e-3, label=label)
        self.vx_subplot.add_line(dt, state.dx * 1e-3, label=label)
        self.vy_subplot.add_line(dt, state.dy * 1e-3, label=label)
        self.vz_subplot.add_line(dt, state.dz * 1e-3, label=label)

        return None

    def plot(self, time: Vector, state: CartesianState) -> str:
        """Plot evolution of classical keplerian elements

        :param time: Time vector [s]
        :param state: Keplerian state
        """

        self.add_line(time, state)

        return self.__call__()

    def __call__(self) -> str:

        self.x_subplot()
        self.y_subplot()
        self.z_subplot()
        self.vx_subplot()
        self.vy_subplot()
        self.vz_subplot()
        return super().__call__()


class CompareCartesianOrbits(MultiPlot):

    def __init__(self, setup: PlotSetup = PlotSetup()) -> None:

        if setup.xlabel is not None:
            _xlabel = setup.xlabel
        else:
            _xlabel = "Days past initial epoch"

        setup.subplots = (3, 2)

        base_setup = PlotSetup(
            xlabel=_xlabel,
            grid=setup.grid,
            legend=setup.legend,
        )

        self.x_setup = base_setup.copy()
        self.x_setup.ylabel = r"$\Delta x$ [km]"

        self.y_setup = base_setup.copy()
        self.y_setup.ylabel = r"$\Delta y$ [km]"

        self.z_setup = base_setup.copy()
        self.z_setup.ylabel = r"$\Delta z$ [km]"

        self.vx_setup = base_setup.copy()
        self.vx_setup.ylabel = r"$\Delta \dot x$ [km/s]"

        self.vy_setup = base_setup.copy()
        self.vy_setup.ylabel = r"$\Delta \dot y$ [km/s]"

        self.vz_setup = base_setup.copy()
        self.vz_setup.ylabel = r"$\Delta \dot z$ [km/s]"

        super().__init__(setup)

        # Generate subplots
        self.x_subplot = self.add_plot(self.x_setup)
        self.y_subplot = self.add_plot(self.y_setup)
        self.z_subplot = self.add_plot(self.z_setup)
        self.vx_subplot = self.add_plot(self.vx_setup)
        self.vy_subplot = self.add_plot(self.vy_setup)
        self.vz_subplot = self.add_plot(self.vz_setup)

        return None

    def add_line(
        self,
        time: Vector,
        orbit: CartesianState,
        reference: CartesianState,
        fmt: str = "-",
        label: str | None = None,
    ) -> None:

        dt = (time - time[0]) / (24.0 * 3600.0)
        ds = orbit - reference

        self.x_subplot.add_line(dt, ds.x * 1e-3, fmt=fmt, label=label)
        self.y_subplot.add_line(dt, ds.y * 1e-3, fmt=fmt, label=label)
        self.z_subplot.add_line(dt, ds.z * 1e-3, fmt=fmt, label=label)
        self.vx_subplot.add_line(dt, ds.dx * 1e-3, fmt=fmt, label=label)
        self.vy_subplot.add_line(dt, ds.dy * 1e-3, fmt=fmt, label=label)
        self.vz_subplot.add_line(dt, ds.dz * 1e-3, fmt=fmt, label=label)

        return None

    def plot(
        self, time: Vector, orbit: CartesianState, reference: CartesianState
    ) -> str:
        """Plot difference between two sets of cartesian state vectors

        :param time: Time vector [s]
        :param orbit: Cartesian states of orbit.
        :param reference: Cartesian states of reference orbit.
        """

        self.add_line(time, orbit, reference)

        return self.__call__()

    def __call__(self) -> str:

        self.x_subplot()
        self.y_subplot()
        self.z_subplot()
        self.vx_subplot()
        self.vy_subplot()
        self.vz_subplot()

        return super().__call__()


class CompareKeplerianOrbits(MultiPlot):

    def __init__(self, setup: PlotSetup = PlotSetup()) -> None:

        if setup.xlabel is not None:
            _xlabel = setup.xlabel
        else:
            _xlabel = "Days past initial epoch"

        setup.subplots = (3, 2)

        base_setup = PlotSetup(xlabel=_xlabel, grid=setup.grid, legend=setup.legend)

        self.a_setup = base_setup.copy()
        self.a_setup.ylabel = r"$\Delta a$ [km]"

        self.e_setup = base_setup.copy()
        self.e_setup.ylabel = r"$\Delta e$"

        self.i_setup = base_setup.copy()
        self.i_setup.ylabel = r"$\Delta i$ [deg]"

        self.omega_setup = base_setup.copy()
        self.omega_setup.ylabel = r"$\Delta \omega$ [deg]"

        self.Omega_setup = base_setup.copy()
        self.Omega_setup.ylabel = r"$\Delta \Omega$ [deg]"

        self.nu_setup = base_setup.copy()
        self.nu_setup.ylabel = r"$\Delta \nu$ [deg]"

        super().__init__(setup)

        # Subplots
        self.a_subplot = self.add_plot(self.a_setup)
        self.e_subplot = self.add_plot(self.e_setup)
        self.i_subplot = self.add_plot(self.i_setup)
        self.omega_subplot = self.add_plot(self.omega_setup)
        self.Omega_subplot = self.add_plot(self.Omega_setup)
        self.nu_subplot = self.add_plot(self.nu_setup)

        return None

    def add_line(
        self,
        time: Vector,
        orbit: KeplerianState,
        reference: KeplerianState,
        fmt: str = "-",
        label: str | None = None,
    ) -> None:

        dt = (time - time[0]) / (24.0 * 3600.0)
        ds = orbit - reference

        self.a_subplot.add_line(dt, ds.a * 1e-3, fmt=fmt, label=label)
        self.e_subplot.add_line(dt, ds.e, fmt=fmt, label=label)
        self.i_subplot.add_line(dt, ds.i, fmt=fmt, label=label)
        self.omega_subplot.add_line(dt, ds.omega, fmt=fmt, label=label)
        self.Omega_subplot.add_line(dt, ds.Omega, fmt=fmt, label=label)
        self.nu_subplot.add_line(dt, ds.nu, fmt=fmt, label=label)

        return None

    def plot(
        self, time: Vector, orbit: KeplerianState, reference: KeplerianState
    ) -> str:
        """Plot difference between two sets of keplerian state vectors

        :param time: Time vector [s]
        :param orbit: Keplerian states of orbit.
        :param reference: Keplerian states of reference orbit.
        """
        self.add_line(time, orbit, reference)

        return self.__call__()

    def __call__(self) -> str:

        self.a_subplot()
        self.e_subplot()
        self.i_subplot()
        self.omega_subplot()
        self.Omega_subplot()
        self.nu_subplot()

        return super().__call__()


class PlotRVMagnitudes(MultiPlot):
    """Plot the magnitude of the position and velocity vectors"""

    def __init__(self, setup: PlotSetup = PlotSetup()) -> None:

        if setup.xlabel is None:
            _xlabel = "Days past initial epoch"
        else:
            _xlabel = setup.xlabel

        setup.subplots = (2, 1)

        base_setup = PlotSetup(xlabel=_xlabel, grid=setup.grid, legend=setup.legend)

        self.r_setup = base_setup.copy()
        self.r_setup.ylabel = r"$\| \vec{r} \|$ [km]"

        self.v_setup = base_setup.copy()
        self.v_setup.ylabel = r"$\| \vec{v} \|$ [km/s]"

        super().__init__(setup)

        # Initialize subplots
        self.r_subplot = self.add_plot(self.r_setup)
        self.v_subplot = self.add_plot(self.v_setup)

        return None

    def add_line(
        self, time: Vector, state: CartesianState, label: str | None = None
    ) -> None:

        dt = (time - time[0]) / (24.0 * 3600.0)

        self.r_subplot.add_line(dt, state.r_mag * 1e-3, label=label)
        self.v_subplot.add_line(dt, state.u_mag * 1e-3, label=label)

        return None

    def plot(self, time: Vector, state: CartesianState) -> str:
        """Plot magnitude of position and velocity vectors

        :param time: Time vector [s]
        :param state: Cartesian states of orbit.
        """

        self.add_line(time, state)

        return self.__call__()

    def __call__(self) -> str:

        self.r_subplot()
        self.v_subplot()
        return super().__call__()


class CompareRVMagnitudes(MultiPlot):

    def __init__(self, setup: PlotSetup = PlotSetup()) -> None:

        setup.subplots = (2, 1)

        base_setup = setup.copy()
        base_setup.show = False
        base_setup.save = False
        if setup.xlabel is None:
            base_setup.xlabel = "Days past initial epoch"

        self.range_setup = base_setup.copy()
        self.range_setup.ylabel = r"$\Delta \rho$ [km]"

        self.rate_setup = base_setup.copy()
        self.rate_setup.ylabel = r"$\Delta \dot \rho$ [km/s]"

        super().__init__(setup)

        # Initialize subplots
        self.range_subplot = self.add_plot(self.range_setup)
        self.rate_subplot = self.add_plot(self.rate_setup)

        return None

    def add_line(
        self,
        time: Vector,
        orbit: CartesianState,
        reference: CartesianState,
        label: str | None = None,
    ) -> None:

        dt = (time - time[0]) / (24.0 * 3600.0)
        ds = orbit - reference

        self.range_subplot.add_line(dt, ds.r_mag * 1e-3, label=label)
        self.rate_subplot.add_line(dt, ds.u_mag * 1e-3, label=label)

        return None

    def plot(
        self, time: Vector, orbit: CartesianState, reference: CartesianState
    ) -> str:
        """Plot magnitude of the difference in position and velocity between
        two sets of cartesian state vectors

        :param time: Time vector [s]
        :param orbit: Cartesian states of orbit.
        :param reference: Cartesian states of reference orbit.
        """
        self.add_line(time, orbit, reference)

        return self.__call__()

    def __call__(self) -> str:

        self.range_subplot()
        self.rate_subplot()
        return super().__call__()


class PlotOrbit(Base3D):

    def add_orbit(
        self, state: CartesianState, label: str | None = None, fmt: str = "-"
    ) -> None:

        self.add_line(state.x, state.y, state.z, fmt, label=label)

        return None

    def plot(self, state: CartesianState) -> str:
        """Plot 3D orbit

        :param state: Cartesian states of orbit.
        """

        self.add_orbit(state)

        return self.postprocess()


# class PlotCartesianState(MultiPlot):
#     """Plot evolution of cartesian state components"""

#     def __init__(self, setup: PlotSetup) -> None:

#         if setup.xlabel is None:
#             _xlabel = "Days past initial epoch"
#         else:
#             _xlabel = setup.xlabel

#         setup.subplots = (3, 2)

#         x_setup = PlotSetup(ylabel="$x$ [km]", xlabel=_xlabel)
#         y_setup = PlotSetup(ylabel="$y$ [km]", xlabel=_xlabel)
#         z_setup = PlotSetup(ylabel="$z$ [km]", xlabel=_xlabel)
#         vx_setup = PlotSetup(ylabel="$v_x$ [km/s]", xlabel=_xlabel)
#         vy_setup = PlotSetup(ylabel="$v_y$ [km/s]", xlabel=_xlabel)
#         vz_setup = PlotSetup(ylabel="$v_z$ [km/s]", xlabel=_xlabel)

#         subplot_setups: list[PlotSetup] = [
#             x_setup,
#             y_setup,
#             z_setup,
#             vx_setup,
#             vy_setup,
#             vz_setup,
#         ]

#         super().__init__(setup, subplot_setups, GenericPlot)

#         return None

#     def plot(self, time: Vector, state: CartesianState) -> None:
#         """Plot evolution of classical keplerian elements

#         :param time: Time vector [s]
#         :param state: Keplerian state
#         """

#         # Turn time vector into days past initial epoch
#         dt = (time - time[0]) / (24.0 * 3600.0)

#         self.generators[0].plot(dt, state.x * 1e-3)  # x [m] -> [km]
#         self.generators[1].plot(dt, state.y * 1e-3)  # y [m] -> [km]
#         self.generators[2].plot(dt, state.z * 1e-3)  # z [m] -> [km]
#         self.generators[3].plot(dt, state.dx * 1e-3)  # dx [m/s] -> [km/s]
#         self.generators[4].plot(dt, state.dy * 1e-3)  # dy [m/s] -> [km/s]
#         self.generators[5].plot(dt, state.dz * 1e-3)  # dz [m/s] -> [km/s]

#         self._post()

#         return None


# class CompareCartesian(MultiPlot):
#     """Compare two sets of cartesian states"""

#     def __init__(self, setup: PlotSetup) -> None:

#         if setup.xlabel is None:
#             _xlabel = "Days past initial epoch"
#         else:
#             _xlabel = setup.xlabel

#         setup.subplots = (3, 2)

#         x_setup = PlotSetup(ylabel=r"$\Delta x$ [km]", xlabel=_xlabel)
#         y_setup = PlotSetup(ylabel=r"$\Delta y$ [km]", xlabel=_xlabel)
#         z_setup = PlotSetup(ylabel=r"$\Delta z$ [km]", xlabel=_xlabel)
#         dx_setup = PlotSetup(ylabel=r"$\Delta \dot x$ [km/s]", xlabel=_xlabel)
#         dy_setup = PlotSetup(ylabel=r"$\Delta \dot y$ [km/s]", xlabel=_xlabel)
#         dz_setup = PlotSetup(ylabel=r"$\Delta \dot z$ [km/s]", xlabel=_xlabel)

#         subplot_setups: list[PlotSetup] = [
#             x_setup,
#             y_setup,
#             z_setup,
#             dx_setup,
#             dy_setup,
#             dz_setup,
#         ]

#         super().__init__(setup, subplot_setups, GenericPlot)

#         return None

#     def plot(
#         self, time: Vector, target: CartesianState, reference: CartesianState
#     ) -> None:
#         """Plot difference between two sets of cartesian state vectors

#         :param time: Time vector [s]
#         :param target: Cartesian states of orbit.
#         :param reference: Cartesian states of reference orbit.
#         """

#         # Turn time vector into days past initial epoch
#         dt = (time - time[0]) / (24.0 * 3600.0)

#         self.generators[0].plot(dt, (target.x - reference.x) * 1e-3)
#         self.generators[1].plot(dt, (target.y - reference.y) * 1e-3)
#         self.generators[2].plot(dt, (target.z - reference.z) * 1e-3)
#         self.generators[3].plot(dt, (target.dx - reference.dx) * 1e-3)
#         self.generators[4].plot(dt, (target.dy - reference.dy) * 1e-3)
#         self.generators[5].plot(dt, (target.dz - reference.dz) * 1e-3)

#         self._post()

#         return None


# class PlotRVMagnitudes(MultiPlot):
#     """Plot the magnitude of the position and velocity vectors"""

#     def __init__(self, setup: PlotSetup) -> None:

#         if setup.xlabel is None:
#             _xlabel = "Days past initial epoch"
#         else:
#             _xlabel = setup.xlabel

#         setup.subplots = (2, 1)

#         r_setup = PlotSetup(ylabel=r"$\| \vec{r} \|$ [km]", xlabel=_xlabel)
#         v_setup = PlotSetup(ylabel=r"$\| \vec{v} \|$ [km/s]", xlabel=_xlabel)

#         subplot_setups: list[PlotSetup] = [r_setup, v_setup]
#         super().__init__(setup, subplot_setups, GenericPlot)

#         return None

#     def plot(self, time: Vector, state: CartesianState) -> None:
#         """Plot magnitude of position and velocity vectors

#         :param time: Time vector [s]
#         :param state: Cartesian states of orbit.
#         """

#         # Turn time vector into days past initial epoch
#         dt = (time - time[0]) / (24.0 * 3600.0)

#         self.generators[0].plot(dt, state.r_mag * 1e-3)  # r [m] -> [km]
#         self.generators[1].plot(dt, state.u_mag * 1e-3)  # v [m/s] -> [km/s]

#         self._post()

#         return None


# NOTE: NOT WORKING PROPERLY
# class PlotGroundTrack(MultiPlot):
#     """Plot ground track and orbital radius"""

#     def __init__(self, setup: PlotSetup) -> None:

#         if setup.xlabel is None:
#             _xlabel = "Days past initial epoch"
#         else:
#             _xlabel = setup.xlabel

#         setup.subplots = (2, 1)

#         r_setup = PlotSetup(ylabel="Orbital radius [km]", xlabel=_xlabel)
#         track_setup = PlotSetup(ylabel="Latitude [deg]",
#                                 xlabel="Longitude [deg]")

#         subplot_setups = [r_setup, track_setup]
#         super().__init__(setup, subplot_setups, SinglePlot)

#         return None

#     def plot(self, time: Vector, state: SphericalGeocentric):
#         """Plot ground track and orbital radius

#         :param time: Time vector [s]
#         :param state: Spherical geocentric states of orbit.
#         """

#         # Turn time vector into days past initial epoch
#         dt = (time - time[0]) / (24. * 3600.)

#         # Remove discontinuities in longitude
#         assert isinstance(state.lon, np.ndarray)
#         diff = (state.lon[:-1] - state.lon[1:]) > 190.
#         diff = np.concatenate((diff, [False]))
#         state.lon[diff] = np.nan

#         self.generators[0].plot(dt, state.r * 1e-3)    # r [m] -> [km]
#         self.generators[1].plot(state.lon, state.lat)
#         self.axes[1].set_xlim(-180, 181)

#         self._post()

#         return None
