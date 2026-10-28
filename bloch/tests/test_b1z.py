import unittest

import numpy as np

from bloch import bloch


GAMMA_RAD_S_PER_G = 26753.0
TWOPI_IMPLEMENTATION = 6.283185


class LongitudinalFieldTests(unittest.TestCase):
    def setUp(self):
        self.b1 = np.array([0.001 + 0.0002j, 0.0007 - 0.0001j, 0.0j, 0.0004j])
        self.gradient = np.zeros(self.b1.size)
        self.dt_s = 4e-6
        self.initial = (
            np.array([0.2]),
            np.array([-0.1]),
            np.array([0.95]),
        )

    def run_bloch(self, *, b1z, df=37.0):
        return bloch(
            self.b1,
            self.gradient,
            self.dt_s,
            1.2,
            0.08,
            df,
            0.0,
            2,
            *self.initial,
            b1z=b1z,
        )

    def test_none_matches_explicit_zero_vector(self):
        implicit = self.run_bloch(b1z=None)
        explicit = self.run_bloch(b1z=np.zeros(self.b1.size))

        for implicit_component, explicit_component in zip(implicit, explicit):
            np.testing.assert_array_equal(implicit_component, explicit_component)

    def test_constant_b1z_matches_positive_off_resonance_shift(self):
        amplitude_g = 0.003
        equivalent_df_hz = amplitude_g * GAMMA_RAD_S_PER_G / TWOPI_IMPLEMENTATION

        via_b1z = self.run_bloch(b1z=np.full(self.b1.size, amplitude_g), df=0.0)
        via_df = self.run_bloch(b1z=None, df=equivalent_df_hz)

        for b1z_component, df_component in zip(via_b1z, via_df):
            np.testing.assert_allclose(b1z_component, df_component, rtol=0.0, atol=2e-15)

    def test_time_varying_b1z_matches_analytical_z_rotation(self):
        b1z = np.array([0.001, -0.002, 0.003, 0.0005])
        transverse_initial = (
            np.array([1.0]),
            np.array([0.0]),
            np.array([0.0]),
        )
        mx, my, mz = bloch(
            np.zeros(b1z.size, dtype=complex),
            np.zeros(b1z.size),
            self.dt_s,
            1e30,
            1e30,
            0.0,
            0.0,
            2,
            *transverse_initial,
            b1z=b1z,
        )

        angle_rad = np.cumsum(-GAMMA_RAD_S_PER_G * b1z * self.dt_s)
        np.testing.assert_allclose(mx, np.cos(angle_rad), rtol=0.0, atol=2e-15)
        np.testing.assert_allclose(my, np.sin(angle_rad), rtol=0.0, atol=2e-15)
        np.testing.assert_allclose(mz, np.zeros_like(angle_rad), rtol=0.0, atol=2e-15)

    def test_b1z_length_must_match_transverse_rf(self):
        with self.assertRaisesRegex(ValueError, "same length as b1"):
            self.run_bloch(b1z=np.zeros(self.b1.size - 1))


if __name__ == "__main__":
    unittest.main()

