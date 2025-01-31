from copy import copy

import numpy as np
from scipy.integrate import DenseOutput, OdeSolver
from scipy.integrate._ivp.common import (
    select_initial_step,
    validate_max_step,
    validate_tol,
    warn_extraneous,
)

A = [
    np.array([]),
    np.array([5.26001519587677318785587544488e-2]),
    np.array([1.97250569845378994544595329183e-2, 5.91751709536136983633785987549e-2]),
    np.array(
        [2.95875854768068491816892993775e-2, 0, 8.87627564304205475450678981324e-2]
    ),
    np.array(
        [
            2.41365134159266685502369798665e-1,
            0,
            -8.84549479328286085344864962717e-1,
            9.24834003261792003115737966543e-1,
        ]
    ),
    np.array(
        [
            3.7037037037037037037037037037e-2,
            0,
            0,
            1.70828608729473871279604482173e-1,
            1.25467687566822425016691814123e-1,
        ]
    ),
    np.array(
        [
            3.7109375e-2,
            0,
            0,
            1.70252211019544039314978060272e-1,
            6.02165389804559606850219397283e-2,
            -1.7578125e-2,
        ]
    ),
    np.array(
        [
            3.70920001185047927108779319836e-2,
            0,
            0,
            1.70383925712239993810214054705e-1,
            1.07262030446373284651809199168e-1,
            -1.53194377486244017527936158236e-2,
            8.27378916381402288758473766002e-3,
        ]
    ),
    np.array(
        [
            6.24110958716075717114429577812e-1,
            0,
            0,
            -3.36089262944694129406857109825e-0,
            -8.68219346841726006818189891453e-1,
            2.75920996994467083049415600797e1,
            2.01540675504778934086186788979e1,
            -4.34898841810699588477366255144e1,
        ]
    ),
    np.array(
        [
            4.77662536438264365890433908527e-1,
            0,
            0,
            -2.48811461997166764192642586468e-0,
            -5.90290826836842996371446475743e-1,
            2.12300514481811942347288949897e1,
            1.52792336328824235832596922938e1,
            -3.32882109689848629194453265587e1,
            -2.03312017085086261358222928593e-2,
        ]
    ),
    np.array(
        [
            -9.3714243008598732571704021658e-1,
            0,
            0,
            5.18637242884406370830023853209e0,
            1.09143734899672957818500254654e0,
            -8.14978701074692612513997267357e0,
            -1.85200656599969598641566180701e1,
            2.27394870993505042818970056734e1,
            2.49360555267965238987089396762e0,
            -3.0467644718982195003823669022e0,
        ]
    ),
    np.array(
        [
            2.27331014751653820792359768449e0,
            0,
            0,
            -1.05344954667372501984066689879e1,
            -2.00087205822486249909675718444e0,
            -1.79589318631187989172765950534e1,
            2.79488845294199600508499808837e1,
            -2.85899827713502369474065508674e0,
            -8.87285693353062954433549289258e0,
            1.23605671757943030647266201528e1,
            6.43392746015763530355970484046e-1,
        ]
    ),
    np.array([]),
    np.array(
        [
            5.61675022830479523392909219681e-2,
            0,
            0,
            0,
            0,
            0,
            2.53500210216624811088794765333e-1,
            -2.46239037470802489917441475441e-1,
            -1.24191423263816360469010140626e-1,
            1.5329179827876569731206322685e-1,
            8.20105229563468988491666602057e-3,
            7.56789766054569976138603589584e-3,
            -8.298e-3,
        ]
    ),
    np.array(
        [
            3.18346481635021405060768473261e-2,
            0,
            0,
            0,
            0,
            2.83009096723667755288322961402e-2,
            5.35419883074385676223797384372e-2,
            -5.49237485713909884646569340306e-2,
            0,
            0,
            -1.08347328697249322858509316994e-4,
            3.82571090835658412954920192323e-4,
            -3.40465008687404560802977114492e-4,
            1.41312443674632500278074618366e-1,
        ]
    ),
    np.array(
        [
            -4.28896301583791923408573538692e-1,
            0,
            0,
            0,
            0,
            -4.69762141536116384314449447206e0,
            7.68342119606259904184240953878e0,
            4.06898981839711007970213554331e0,
            3.56727187455281109270669543021e-1,
            0,
            0,
            0,
            -1.39902416515901462129418009734e-3,
            2.9475147891527723389556272149e0,
            -9.15095847217987001081870187138e0,
        ]
    ),
]

C = np.array(
    [
        0.0,
        0.526001519587677318785587544488e-01,
        0.789002279381515978178381316732e-01,
        0.118350341907227396726757197510e00,
        0.281649658092772603273242802490e00,
        0.333333333333333333333333333333e00,
        0.25e00,
        0.307692307692307692307692307692e00,
        0.651282051282051282051282051282e00,
        0.6e00,
        0.857142857142857142857142857142e00,
        1.0,
        1.0,
        0.1e00,
        0.2e00,
        0.777777777777777777777777777778e00,
    ]
)

B = np.array(
    [
        5.42937341165687622380535766363e-2,
        0,
        0,
        0,
        0,
        4.45031289275240888144113950566e0,
        1.89151789931450038304281599044e0,
        -5.8012039600105847814672114227e0,
        3.1116436695781989440891606237e-1,
        -1.52160949662516078556178806805e-1,
        2.01365400804030348374776537501e-1,
        4.47106157277725905176885569043e-2,
    ]
)


BHH = np.array(
    [
        0.244094488188976377952755905512e00,
        0.733846688281611857341361741547e00,
        0.220588235294117647058823529412e-01,
    ]
)

E = np.array(
    [
        0.1312004499419488073250102996e-01,
        0,
        0,
        0,
        0,
        -0.1225156446376204440720569753e01,
        -0.4957589496572501915214079952e00,
        0.1664377182454986536961530415e01,
        -0.3503288487499736816886487290e00,
        0.3341791187130174790297318841e00,
        0.8192320648511571246570742613e-01,
        -0.2235530786388629525884427845e-01,
    ]
)

D = [
    np.array([]),
    np.array([]),
    np.array([]),
    np.array([]),
    np.array(
        [
            -0.84289382761090128651353491142e01,
            0,
            0,
            0,
            0,
            0.56671495351937776962531783590e00,
            -0.30689499459498916912797304727e01,
            0.23846676565120698287728149680e01,
            0.21170345824450282767155149946e01,
            -0.87139158377797299206789907490e00,
            0.22404374302607882758541771650e01,
            0.63157877876946881815570249290e00,
            -0.88990336451333310820698117400e-01,
            0.18148505520854727256656404962e02,
            -0.91946323924783554000451984436e01,
            -0.44360363875948939664310572000e01,
        ]
    ),
    np.array(
        [
            0.10427508642579134603413151009e02,
            0,
            0,
            0,
            0,
            0.24228349177525818288430175319e03,
            0.16520045171727028198505394887e03,
            -0.37454675472269020279518312152e03,
            -0.22113666853125306036270938578e02,
            0.77334326684722638389603898808e01,
            -0.30674084731089398182061213626e02,
            -0.93321305264302278729567221706e01,
            0.15697238121770843886131091075e02,
            -0.31139403219565177677282850411e02,
            -0.93529243588444783865713862664e01,
            0.35816841486394083752465898540e02,
        ]
    ),
    np.array(
        [
            0.19985053242002433820987653617e02,
            0,
            0,
            0,
            0,
            -0.38703730874935176555105901742e03,
            -0.18917813819516756882830838328e03,
            0.52780815920542364900561016686e03,
            -0.11573902539959630126141871134e02,
            0.68812326946963000169666922661e01,
            -0.10006050966910838403183860980e01,
            0.77771377980534432092869265740e00,
            -0.27782057523535084065932004339e01,
            -0.60196695231264120758267380846e02,
            0.84320405506677161018159903784e02,
            0.11992291136182789328035130030e02,
        ]
    ),
    np.array(
        [
            -0.25693933462703749003312586129e02,
            0,
            0,
            0,
            0,
            -0.15418974869023643374053993627e03,
            -0.23152937917604549567536039109e03,
            0.35763911791061412378285349910e03,
            0.93405324183624310003907691704e02,
            -0.37458323136451633156875139351e02,
            0.10409964950896230045147246184e03,
            0.29840293426660503123344363579e02,
            -0.435334565900111437544321750583e02,
            0.96324553959188282948394950600e02,
            -0.39177261675615439165231486172e02,
            -0.14972683625798562581422125276e03,
        ]
    ),
]


def validate_max_nsteps(max_nsteps):
    if max_nsteps <= 0:
        raise ValueError("`max_nsteps` must be positive.")
    return max_nsteps


def validate_safety_factor(safety_factor):
    if safety_factor >= 1.0 or safety_factor <= 1e-4:
        raise ValueError("`safety_factor` must lie within 1e-4 and 1.0.")
    return safety_factor


def validate_beta_stabilizer(beta_stabilizer):
    if beta_stabilizer < 0 or beta_stabilizer > 0.2:
        raise ValueError("`beta_stabilizer` must lie within 0 and 0.2.")
    return beta_stabilizer


class DOP835(OdeSolver):
    A = A
    C = C
    B = B
    E = E
    BHH = BHH
    D = D

    t: float
    y: np.array

    def __init__(
        self,
        fun,
        t0,
        y0,
        t_bound,
        max_step=np.inf,
        rtol=1e-7,
        atol=1e-12,
        safety_factor=0.9,
        min_step_change=0.333,
        max_step_change=6.0,
        beta_stabilizer=0.00,
        max_nsteps=100000,
        vectorized=False,
        **extraneous
    ):
        warn_extraneous(extraneous)
        super().__init__(fun, t0, y0, t_bound, vectorized, support_complex=True)
        self.y_old = None
        self.max_step = validate_max_step(max_step)
        self.beta_stabilizer = validate_beta_stabilizer(beta_stabilizer)
        self.max_nsteps = validate_max_nsteps(max_nsteps)
        self.safety_factor = validate_safety_factor(safety_factor)
        self.rtol, self.atol = validate_tol(rtol, atol, self.n)
        self.min_step_change = min_step_change
        self.max_step_change = max_step_change
        self.order = 8

        self.f = self.fun(self.t, self.y)
        self.h_abs = select_initial_step(
            self.fun,
            self.t,
            self.y,
            self.f,
            self.direction,
            self.order,
            self.rtol,
            self.atol,
        )
        self.nfev += 2

        self.n_steps = 0
        self.n_accepted = 0
        self.n_rejected = 0
        self.factor_old = 1e-4  # Lund-stabilization factor
        self.K = np.zeros((16, self.n))
        self.interpolation = np.zeros((8, self.n))

    def _step_impl(self):
        t = self.t
        y = self.y
        f = self.f
        K = self.K

        rtol = self.rtol
        atol = self.atol

        min_step = 10 * np.abs(np.nextafter(t, self.direction * np.inf) - t)

        while True:
            if self.h_abs < min_step:
                return False, self.TOO_SMALL_STEP

            h = self.h_abs * self.direction
            t_new = t + h

            if self.direction * (t_new - self.t_bound) > 0:
                t_new = self.t_bound

            h = t_new - t
            h_abs = np.abs(h)

            K[0] = f
            for s in range(1, 12):
                a, c = self.A[s], self.C[s]
                dy = np.dot(K[:s].T, a) * h
                K[s] = self.fun(t + c * h, y + dy)
            self.nfev += 11

            f_B = np.dot(K[:12].T, self.B)
            y_final = y + h * f_B

            scale = atol + np.maximum(np.abs(y), np.abs(y_final)) * rtol
            err_BHH = (
                f_B - self.BHH[0] * K[0] - self.BHH[1] * K[8] - self.BHH[2] * K[11]
            )
            err_BHH = np.sum((err_BHH / scale) ** 2)

            err_E = np.dot(K[:12].T, self.E)
            err_E = np.sum((err_E / scale) ** 2)

            denominator = err_E + 1e-2 * err_BHH
            err_E = h_abs * err_E / np.sqrt(self.n * denominator)

            err_exp = err_E ** (0.125 - self.beta_stabilizer * 0.2)
            dh_factor = err_exp / (self.factor_old ** self.beta_stabilizer)
            dh_factor = np.max(
                [
                    1.0 / self.max_step_change,
                    np.min(
                        [1.0 / self.min_step_change, dh_factor / self.safety_factor]
                    ),
                ]
            )
            h_new_abs = h_abs / dh_factor

            if err_E < 1.0:
                self.factor_old = np.max([err_E, 1e-4])
                self.n_accepted += 1
                K[12] = self.fun(t + h, y_final)

                for s in range(13, 16):
                    a, c = self.A[s], self.C[s]
                    dy = np.dot(K[:s].T, a) * h
                    K[s] = self.fun(t + c * h, y + dy)
                self.nfev += 4

                # prepare the dense output
                self.interpolation[0] = y
                self.interpolation[1] = y_final - y
                self.interpolation[2] = h * K[0] - self.interpolation[1]
                self.interpolation[3] = (
                    self.interpolation[1] - h * K[12] - self.interpolation[2]
                )
                for n in range(4, 8):
                    self.interpolation[n] = h * np.dot(K[:16].T, self.D[n])

                self.y_old = y
                self.t = t_new
                self.y = y_final
                self.f = K[12]
                self.h_abs = h_new_abs

                return True, None
            else:
                self.n_rejected += 1
                self.h_abs /= np.min(
                    [1.0 / self.min_step_change, err_exp / self.safety_factor]
                )

    def _dense_output_impl(self):
        return DOP835DenseOutput(self.t_old, self.t, self.y_old, self.interpolation)


def get_coeffs(s):
    coeffs = np.zeros((8))
    s_back = 1.0 - s
    coeffs[0] = 1.0
    for i in range(7):
        if i % 2 == 0:
            coeffs[i + 1] = coeffs[i] * s
        else:
            coeffs[i + 1] = coeffs[i] * s_back
    return np.array(coeffs)


class DOP835DenseOutput(DenseOutput):
    def __init__(self, t_old, t_new, y_old, interpolation):
        super().__init__(t_old, t_new)
        self.h = t_new - t_old
        self.interpolation = copy(interpolation)
        self.y_old = y_old

    def _call_impl(self, t_eval):
        s = (t_eval - self.t_old) / self.h
        coeffs = get_coeffs(s)
        return np.dot(self.interpolation.T, coeffs)
