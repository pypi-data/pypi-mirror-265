#include "pantr-params.hpp"

template <alpaqa::Config Conf>
PARAMS_TABLE_DEF(alpaqa::PANTRParams<Conf>,                                     //
                 PARAMS_MEMBER(Lipschitz),                                      //
                 PARAMS_MEMBER(max_iter),                                       //
                 PARAMS_MEMBER(max_time),                                       //
                 PARAMS_MEMBER(L_min),                                          //
                 PARAMS_MEMBER(L_max),                                          //
                 PARAMS_MEMBER(stop_crit),                                      //
                 PARAMS_MEMBER(max_no_progress),                                //
                 PARAMS_MEMBER(print_interval),                                 //
                 PARAMS_MEMBER(print_precision),                                //
                 PARAMS_MEMBER(quadratic_upperbound_tolerance_factor),          //
                 PARAMS_MEMBER(TR_tolerance_factor),                            //
                 PARAMS_MEMBER(ratio_threshold_acceptable),                     //
                 PARAMS_MEMBER(ratio_threshold_good),                           //
                 PARAMS_MEMBER(radius_factor_rejected),                         //
                 PARAMS_MEMBER(radius_factor_acceptable),                       //
                 PARAMS_MEMBER(radius_factor_good),                             //
                 PARAMS_MEMBER(initial_radius),                                 //
                 PARAMS_MEMBER(min_radius),                                     //
                 PARAMS_MEMBER(compute_ratio_using_new_stepsize),               //
                 PARAMS_MEMBER(update_direction_on_prox_step),                  //
                 PARAMS_MEMBER(recompute_last_prox_step_after_direction_reset), //
                 PARAMS_MEMBER(disable_acceleration),                           //
                 PARAMS_MEMBER(ratio_approx_fbe_quadratic_model),               //
);

PARAMS_TABLE_INST(alpaqa::PANTRParams<alpaqa::EigenConfigd>);
ALPAQA_IF_FLOAT(PARAMS_TABLE_INST(alpaqa::PANTRParams<alpaqa::EigenConfigf>);)
ALPAQA_IF_LONGD(PARAMS_TABLE_INST(alpaqa::PANTRParams<alpaqa::EigenConfigl>);)
ALPAQA_IF_QUADF(PARAMS_TABLE_INST(alpaqa::PANTRParams<alpaqa::EigenConfigq>);)
