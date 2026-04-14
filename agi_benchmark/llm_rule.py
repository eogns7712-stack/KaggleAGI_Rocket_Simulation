# llm_rule.py

class RuleBasedLLM:
    def predict(self, state, valid_actions):
        phase = state.get("mission_phase")

        # -----------------------------
        # Phase 1
        # -----------------------------
        if phase == 1:
            if (
                not state.get("is_launched", False)
                and state.get("launch_ready", False)
                and "LAUNCH" in valid_actions
            ):
                return "LAUNCH"

            if (
                state.get("is_launched", False)
                and not state.get("escaped_earth", False)
                and state.get("fuel_s1", 0) > 0
                and "CONTINUE_BURN" in valid_actions
            ):
                return "CONTINUE_BURN"

            if "WAIT" in valid_actions:
                return "WAIT"

        # -----------------------------
        # Phase 2
        # -----------------------------
        if phase == 2:
            if (
                state.get("escaped_earth", False)
                and state.get("fuel_s1", 1) == 0
                and state.get("is_stage1_attached", False)
                and "SEPARATE_S1" in valid_actions
            ):
                return "SEPARATE_S1"

            if (
                state.get("escaped_earth", False)
                and not state.get("near_europa", False)
                and not state.get("is_stage1_attached", False)
                and "MOVE_TO_EUROPA" in valid_actions
            ):
                return "MOVE_TO_EUROPA"

            if "WAIT" in valid_actions:
                return "WAIT"

        # -----------------------------
        # Phase 3
        # -----------------------------
        if phase == 3:
            if (
                state.get("near_europa", False)
                and not state.get("in_europa_orbit", False)
                and state.get("fuel_s2", 0) > 0
                and "IGNITE_S2" in valid_actions
            ):
                return "IGNITE_S2"

            if (
                state.get("in_europa_orbit", False)
                and state.get("fuel_s2", 1) == 0
                and state.get("is_stage2_attached", False)
                and "SEPARATE_S2" in valid_actions
            ):
                return "SEPARATE_S2"

            if (
                state.get("landing", False)
                and state.get("descent_rate_high", False)
                and "CONTROL_BOOSTER" in valid_actions
            ):
                return "CONTROL_BOOSTER"

            if (
                state.get("landing", False)
                and state.get("bad_balance", False)
                and "ADJUST_BALANCE" in valid_actions
            ):
                return "ADJUST_BALANCE"

            if (
                state.get("approaching_europa", False)
                and not state.get("descent_rate_high", False)
                and not state.get("bad_balance", False)
                and "START_LANDING" in valid_actions
            ):
                return "START_LANDING"

            if "WAIT" in valid_actions:
                return "WAIT"

        # -----------------------------
        # Phase 4
        # -----------------------------
        if phase == 4:
            if (
                state.get("on_europa", False)
                and not state.get("ice_broken", False)
                and "DRILL_ICE" in valid_actions
            ):
                return "DRILL_ICE"

            if (
                state.get("ice_broken", False)
                and not state.get("pipe_inserted", False)
                and "INSERT_PIPE" in valid_actions
            ):
                return "INSERT_PIPE"

            if (
                state.get("pipe_inserted", False)
                and not state.get("water_ready", False)
                and "PUMP_WATER" in valid_actions
            ):
                return "PUMP_WATER"

            if (
                state.get("water_ready", False)
                and not state.get("hydrogen_ready", False)
                and "RUN_ELECTROLYSIS" in valid_actions
            ):
                return "RUN_ELECTROLYSIS"

            if (
                state.get("hydrogen_ready", False)
                and not state.get("fuel_s4_full", False)
                and "FILL_S4" in valid_actions
            ):
                return "FILL_S4"

            if (
                state.get("hydrogen_ready", False)
                and state.get("fuel_s4_full", False)
                and not state.get("fuel_s5_full", False)
                and "FILL_S5" in valid_actions
            ):
                return "FILL_S5"

            if (
                state.get("water_ready", False)
                and state.get("fuel_s4_full", False)
                and state.get("fuel_s5_full", False)
                and not state.get("sample_loaded", False)
                and "TRANSFER_SAMPLE" in valid_actions
            ):
                return "TRANSFER_SAMPLE"

            if (
                state.get("fuel_s4_full", False)
                and state.get("fuel_s5_full", False)
                and state.get("sample_loaded", False)
                and not state.get("valves_closed", False)
                and "CLOSE_VALVES" in valid_actions
            ):
                return "CLOSE_VALVES"

            if "WAIT" in valid_actions:
                return "WAIT"

        # -----------------------------
        # Phase 5
        # -----------------------------
        if phase == 5:
            if (
                state.get("on_europa", False)
                and state.get("fuel_s4_full", False)
                and state.get("fuel_s5_full", False)
                and state.get("sample_loaded", False)
                and state.get("valves_closed", False)
                and "LAUNCH_S4" in valid_actions
            ):
                return "LAUNCH_S4"

            if (
                not state.get("on_europa", False)
                and state.get("stage4_engine_on", False)
                and not state.get("outside_europa_escape", False)
                and state.get("fuel_s4", 0) > 0
                and "CONTINUE_BURN" in valid_actions
            ):
                return "CONTINUE_BURN"

            if "WAIT" in valid_actions:
                return "WAIT"

        # -----------------------------
        # Phase 6
        # -----------------------------
        if phase == 6:
            if (
                state.get("outside_europa_escape", False)
                and state.get("fuel_s4", 1) == 0
                and state.get("is_stage4_attached", False)
                and "SEPARATE_S4" in valid_actions
            ):
                return "SEPARATE_S4"

            if (
                state.get("outside_europa_escape", False)
                and not state.get("is_stage4_attached", False)
                and not state.get("near_earth", False)
                and "MOVE_TO_EARTH" in valid_actions
            ):
                return "MOVE_TO_EARTH"

            if "WAIT" in valid_actions:
                return "WAIT"

        # -----------------------------
        # Phase 7
        # -----------------------------
        if phase == 7:
            if (
                state.get("near_earth", False)
                and state.get("fuel_s5", 1) == 0
                and state.get("is_stage5_attached", False)
                and "SEPARATE_S5" in valid_actions
            ):
                return "SEPARATE_S5"

            if (
                state.get("near_earth", False)
                and not state.get("is_stage5_attached", False)
                and not state.get("in_earth_orbit", False)
                and not state.get("return_engine_on", False)
                and "IGNITE_RETURN" in valid_actions
            ):
                return "IGNITE_RETURN"

            if (
                state.get("in_earth_orbit", False)
                and state.get("return_engine_on", False)
                and "STOP_RETURN_BURN" in valid_actions
            ):
                return "STOP_RETURN_BURN"

            if (
                state.get("descending", False)
                and state.get("descent_rate_high", False)
                and "CONTROL_BOOSTER" in valid_actions
            ):
                return "CONTROL_BOOSTER"

            if (
                state.get("descending", False)
                and state.get("bad_balance", False)
                and "ADJUST_BALANCE" in valid_actions
            ):
                return "ADJUST_BALANCE"

            if (
                state.get("descending", False)
                and not state.get("bad_balance", False)
                and not state.get("descent_rate_high", False)
                and not state.get("return_engine_on", False)
                and "LAND" in valid_actions
            ):
                return "LAND"

            if "WAIT" in valid_actions:
                return "WAIT"

        # 공통 fallback
        if "WAIT" in valid_actions:
            return "WAIT"

        if "ABORT_MISSION" in valid_actions:
            return "ABORT_MISSION"

        return valid_actions[0]