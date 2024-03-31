from math import trunc
from .types import (
    CartesianState,
    KeplerianState,
    SphericalGeocentric,
    Date,
    Vector,
)
import numpy as np


def date2jd(date: Date, frac: bool = False, mjd: bool = False) -> tuple[float, float]:
    """Transform calendar date to Julian date.

    :param date: Epoch as calendar date.
    :param frac: Whether to return the whole and fractional parts of the Julian
    date separately or not. If set to false, both parts are added together and
    returned in the first element of the tuple, with the second being set to
    zero. (default: False)
    :param mjd: Whether to return a modified Julian date (default: False).
    """

    # Get Julian date as integer and fractional part
    # Algorithm from slides 2.16
    C = trunc((date.month - 14) / 12)
    jd0 = date.day - 32075 + trunc(1461 * (date.year + 4800 + C) / 4)
    jd0 += trunc(367 * (date.month - 2 - C * 12) / 12)
    jd0 -= trunc(3 * trunc((date.year + 4900 + C) / 100) / 4)
    jd = jd0 - 0.5
    fr = date.hour / 24.0 + date.minute / 1440.0 + date.second / 86400.0

    # Return based on selected format
    if mjd:
        jd = jd - 2400000.5
    if frac:
        return jd, fr
    else:
        return jd + fr, 0.0


def jd2date(jd: float, frac: float | None, mjd: bool = False) -> tuple[Date, float]:
    """Transform Julian date or modified Julian date to calendar date.

    :param jd: Whole part of the Julian date.
    :param frac: Fractional part of the Julian date. If set to None, the
    fractional part is assumed to be contained in `jd`.
    :param mjd: Whether the given date is a modified Julian date (Default:
    False).
    :return date: Calendar date.
    :return error: Residual after rounding the seconds to the nearest integer.
    """

    # Get JD as a single floating point number
    if mjd:
        jd += 2400000.5
    if frac is None:
        frac = jd - trunc(jd) + 0.5
        jd = jd - frac

    # Algorithm from slides 2.17
    jd0 = jd + 0.5
    L1 = trunc(jd0 + 68569)
    L2 = trunc(4 * L1 / 146097)
    L3 = L1 - trunc((146097 * L2 + 3) / 4)
    L4 = trunc(4000 * (L3 + 1) / 1461001)
    L5 = L3 - trunc(1461 * L4 / 4) + 31
    L6 = trunc(80 * L5 / 2447)
    L7 = trunc(L6 / 11)
    day = L5 - trunc(2447 * L6 / 80)
    month = L6 + 2 - 12 * L7
    year = 100 * (L2 - 49) + L4 + L7
    hour = trunc(frac * 24)
    rem = frac * 24 - hour
    minute = trunc(rem * 60)
    rem = rem * 60 - minute
    second = round(rem * 60)
    error = rem * 60 - second

    return Date(day, month, year, hour, minute, second), error


def cartesian2keplerian(s: CartesianState, mu: float) -> KeplerianState:
    """Convert cartesian state vector to keplerian orbital elements

    :param s: Cartesian state [m, m/s].
    :param mu: Gravitational parameter of central body [m^3/s^2]
    :return: Keplerian orbital elements [m, deg]
    """

    # Semi-major axis
    a = 1.0 / ((2.0 / s.r_mag) - (s.u_mag * s.u_mag / mu))

    # Angular momentum
    h_vec = np.cross(s.r, s.u, axis=0)
    h = np.linalg.norm(h_vec, axis=0)

    # Eccentricity
    e_vec = (np.cross(s.u, h_vec, axis=0) / mu) - (s.r / s.r_mag)
    e = np.linalg.norm(e_vec, axis=0)
    e_uvec = e_vec / e

    # Inclination
    i = np.rad2deg(np.arccos(h_vec[2] / h))

    # N vector
    _z_vec = np.array([np.zeros_like(s.x), np.zeros_like(s.y), np.ones_like(s.z)])
    N_vec = np.cross(_z_vec, h_vec, axis=0)
    Nxy = np.sqrt(N_vec[0] * N_vec[0] + N_vec[1] * N_vec[1])
    N_uvec = N_vec / Nxy

    # RAAN
    Omega = np.rad2deg(np.arctan2(N_vec[1] / Nxy, N_vec[0] / Nxy))

    # Argument of periapsis
    sign_omega_condition = np.sum(np.cross(N_uvec, e_vec, axis=0) * h_vec, axis=0) > 0
    sign_omega = 2 * sign_omega_condition - 1
    omega = np.rad2deg(sign_omega * np.arccos(np.sum(e_uvec * N_uvec, axis=0)))

    # True anomaly
    sign_theta_condition = np.sum(np.cross(e_vec, s.r, axis=0) * h_vec, axis=0) > 0
    sign_theta = 2 * sign_theta_condition - 1
    theta = np.rad2deg(sign_theta * np.arccos(np.sum(s.r * e_uvec / s.r_mag, axis=0)))

    return KeplerianState(a, e, i, Omega, omega, theta)


def keplerian2cartesian(s: KeplerianState, mu: float) -> CartesianState:
    """Convert from keplerian orbital elements to cartesian state vector

    :param s: Keplerian orbital elements [m, deg]
    :param mu: Standard gravitational parameter of central body [m^3/s^2]
    :return: Cartesian state vector [m, m/s]
    """
    # Convert angles to radians
    theta = np.deg2rad(s.nu)
    omega = np.deg2rad(s.omega)
    Omega = np.deg2rad(s.Omega)
    inc = np.deg2rad(s.i)

    # Auxiliary trigonometric relations
    cos_Omega = np.cos(Omega)
    sin_Omega = np.sin(Omega)
    cos_omega = np.cos(omega)
    sin_omega = np.sin(omega)
    cos_i = np.cos(inc)
    sin_i = np.sin(inc)
    cos_theta = np.cos(theta)
    sin_theta = np.sin(theta)

    l1 = cos_Omega * cos_omega - sin_Omega * sin_omega * cos_i
    l2 = -cos_Omega * sin_omega - sin_Omega * cos_omega * cos_i
    m1 = sin_Omega * cos_omega + cos_Omega * sin_omega * cos_i
    m2 = -sin_Omega * sin_omega + cos_Omega * cos_omega * cos_i
    n1 = sin_omega * sin_i
    n2 = cos_omega * sin_i

    # Orbital radius
    r = s.a * (1.0 - s.e * s.e) / (1.0 + s.e * cos_theta)

    # Position in orbital plane
    xi = r * cos_theta
    eta = r * sin_theta

    # Position in 3D space
    x = l1 * xi + l2 * eta
    y = m1 * xi + m2 * eta
    z = n1 * xi + n2 * eta

    # Angular momentum
    H = np.sqrt(mu * s.a * (1.0 - s.e * s.e))

    # Velocity
    common = mu / H
    e_cos_theta = s.e + cos_theta

    dx = common * (l2 * e_cos_theta - l1 * sin_theta)
    dy = common * (m2 * e_cos_theta - m1 * sin_theta)
    dz = common * (n2 * e_cos_theta - n1 * sin_theta)

    return CartesianState(x, y, z, dx, dy, dz)


def cartesian2spherical(t: Vector, s: CartesianState) -> SphericalGeocentric:
    """Convert cartesian state vectors to spherical coordinates.

    :param t: Epoch in which the cartesian state is knonw or time series [JD].
    :param s: Cartesian state [m, m/s].
    :return: Spherical coordinates [m, deg].
    """

    def _constrain_theta(theta: float) -> float:
        """Constain angle to [0, 360) deg.

        :param theta: Angle in degrees.
        """
        while (theta > 360.0) or (theta < -360.0):
            if theta > 360.0:
                theta -= 360.0
            elif theta < -360.0:
                theta += 360.0

        return theta

    # Calculate Julian century wrt to J2000
    T = (t - 2451545.0) / 36525.0

    # Calculate GMST in radians
    # Algorithm from Curtis
    a0 = 100.4606184
    a1 = 36000.77004
    a2 = 0.000387933
    a3 = -2.583e-8

    theta_GMST = a0 + a1 * T + a2 * T * T + a3 * T * T * T

    for idx, theta in enumerate(theta_GMST):
        theta_GMST[idx] = _constrain_theta(theta)
    theta_GMST = np.deg2rad(theta_GMST)

    # Calculate dates from JD

    ut_list = np.zeros_like(t)
    for idx, jd in enumerate(t):
        date, err = jd2date(jd, None)
        assert isinstance(date, Date)
        ut_list[idx] = date.hour * 3600.0 + date.minute * 60.0 + date.second + err

    # Calculate Greenwhich sidereal time at current epoch
    # Earth's rotation speed taken from Horizons
    theta_G = theta_GMST + 0.00007292115 * ut_list

    # Rotate position vector to ECI
    x_ECI = s.x * np.cos(theta_G) + s.y * np.sin(theta_G)
    y_ECI = -s.x * np.sin(theta_G) + s.y * np.cos(theta_G)
    z_ECI = s.z

    # Calculate spherical coordinates
    r = np.sqrt(x_ECI * x_ECI + y_ECI * y_ECI + z_ECI * z_ECI)
    lat = np.rad2deg(np.arcsin(z_ECI / r))
    long = np.rad2deg(np.arctan2(y_ECI, x_ECI))

    return SphericalGeocentric(r, lat, long)

    # return SphericalCoordinates(r, lat, long)


def cartesian2spherical_inertial(s: CartesianState) -> SphericalGeocentric:
    """Convert cartesian state vector to spherical, inertial coordinates

    :param s: Cartesian state [m, m/s]
    :return: Spherical inertial coordinates [m, deg]
    """
    lat = np.rad2deg(np.arcsin(s.z / s.r_mag))
    r_xy = np.sqrt(s.x * s.x + s.y * s.y)
    lon = np.rad2deg(np.arctan2(s.y / r_xy, s.x / r_xy))

    return SphericalGeocentric(s.r_mag, lat, lon)


def time2mean_anomaly(
    epochs: Vector, a: float | Vector, mu: float, M0: float = 0.0
) -> Vector:
    """Calculate mean anomaly from time and semi-major axis.

    :param epochs: Epochs at which to calculate the mean anomaly [s].
    :param a: Semi-major axis of the keplerian orbit [m].
    :param mu: Standard gravitational parameter of central body [m^3/s^2].
    :param M0: Initial mean anomaly [rad].
    :return: Mean anomaly [rad].
    """
    return M0 + (epochs - epochs[0]) * np.sqrt(mu / (a * a * a))


def true2eccentric_anomaly(
    nu: float | Vector, e: float | Vector, rad: bool = False
) -> float | Vector:
    """Calculate eccentric anomaly from true anomaly and eccentricity.

    :param nu: True anomaly [rad].
    :param e: Eccentricity of the keplerian orbit.
    :param rad: Whether the true anomaly is in radians or degrees (default: False).
    :return: Eccentric anomaly [rad].
    """
    if not rad:
        nu = np.deg2rad(nu)

    return 2.0 * np.arctan2(
        np.sqrt(1.0 - e) * np.sin(0.5 * nu), np.sqrt(1.0 + e) * np.cos(0.5 * nu)
    )


def eccentric2true_anomaly(
    E: float | Vector, e: float | Vector, deg: bool = True
) -> float | Vector:
    """Calculate true anomaly from eccentric anomaly and eccentricity.

    :param E: Eccentric anomaly [rad].
    :param e: Eccentricity of the keplerian orbit.
    :param deg: Whether to return the true anomaly in degrees (default: True).
    :return: True anomaly [rad].
    """
    nu = 2.0 * np.arctan2(
        np.sqrt(1.0 + e) * np.sin(0.5 * E), np.sqrt(1.0 - e) * np.cos(0.5 * E)
    )

    if deg:
        return np.rad2deg(nu)
    else:
        return nu


def eccentric2mean_anomaly(E: float | Vector, e: float | Vector) -> float | Vector:
    """Calculate mean anomaly from eccentric anomaly and eccentricity.

    :param E: Eccentric anomaly [rad].
    :param e: Eccentricity of the keplerian orbit.
    :return: Mean anomaly [rad].
    """
    return E - e * np.sin(E)
