#pragma once
#include <string>
#include <map>
#include <cstdint>
#include <iomanip>
#include <variant>
#include <duckdb.hpp>

#include "game.hpp"
#include "ticket.hpp"
#include "demand.hpp"

using std::make_shared;
using std::shared_ptr;
using std::string;
using std::to_string;

struct Aircraft {
    struct PaxConfig {
        enum class Algorithm {
            AUTO,  // NOTE: this should only be used in AircraftRoute::Options::ConfigAlgorithm
            FJY,
            FYJ,
            JFY,
            JYF,
            YJF,
            YFJ
        };

        uint16_t y = 0;
        uint16_t j = 0;
        uint16_t f = 0;
        bool valid = false;
        Algorithm algorithm;

        static inline PaxConfig calc_fjy_conf(const PaxDemand& d_pf, uint16_t capacity);
        static inline PaxConfig calc_fyj_conf(const PaxDemand& d_pf, uint16_t capacity);
        static inline PaxConfig calc_jfy_conf(const PaxDemand& d_pf, uint16_t capacity);
        static inline PaxConfig calc_jyf_conf(const PaxDemand& d_pf, uint16_t capacity);
        static inline PaxConfig calc_yfj_conf(const PaxDemand& d_pf, uint16_t capacity);
        static inline PaxConfig calc_yjf_conf(const PaxDemand& d_pf, uint16_t capacity);

        static PaxConfig calc_pax_conf(
            const PaxDemand& pax_demand,
            uint16_t capacity,
            double distance,
            User::GameMode game_mode = User::GameMode::EASY,
            Aircraft::PaxConfig::Algorithm algorithm = Aircraft::PaxConfig::Algorithm::AUTO
        );
        static const string repr(const PaxConfig& pax_config);
    };

    struct CargoConfig {  // percent
        enum class Algorithm {
            AUTO,  // NOTE: this should only be used in AircraftRoute::Options::ConfigAlgorithm
            L,
            H
        };

        uint8_t l = 0;
        uint8_t h = 0;
        bool valid = false;
        Algorithm algorithm;

        static inline CargoConfig calc_l_conf(
            const CargoDemand& d_pf, uint32_t capacity, uint8_t l_training = 0, uint8_t h_training = 0
        );
        static inline CargoConfig calc_h_conf(
            const CargoDemand& d_pf, uint32_t capacity, uint8_t l_training = 0, uint8_t h_training = 0
        );

        static CargoConfig calc_cargo_conf(
            const CargoDemand& cargo_demand,
            uint32_t capacity,
            uint8_t l_training = 0,
            uint8_t h_training = 0,
            Aircraft::CargoConfig::Algorithm algorithm = Aircraft::CargoConfig::Algorithm::AUTO
        );
        static const string repr(const CargoConfig& cargo_config);
    };

    enum class Type { PAX = 0, CARGO = 1, VIP = 2 };

    enum class SearchType { ALL = 0, ID = 1, SHORTNAME = 2, NAME = 3 };

    using Config = std::variant<PaxConfig, CargoConfig>;

    uint16_t id;
    string shortname;
    string manufacturer;
    string name;
    Type type;
    uint8_t priority;
    uint16_t eid;
    string ename;
    float speed;
    float fuel;
    float co2;
    uint32_t cost;
    uint32_t capacity;
    uint16_t rwy;
    uint32_t check_cost;
    uint16_t range;
    uint16_t ceil;
    uint16_t maint;
    uint8_t pilots;
    uint8_t crew;
    uint8_t engineers;
    uint8_t technicians;
    string img;
    uint8_t wingspan;
    uint8_t length;
    bool speed_mod;
    bool fuel_mod;
    bool co2_mod;
    bool fourx_mod;
    bool valid;

    struct ParseResult {
        Aircraft::SearchType search_type;
        string search_str;
        uint8_t priority;
        bool speed_mod;
        bool fuel_mod;
        bool co2_mod;
        bool fourx_mod;

        ParseResult(
            Aircraft::SearchType search_type,
            const string& search_str,
            uint8_t priority,
            bool speed_mod,
            bool fuel_mod,
            bool co2_mod,
            bool fourx_mod
        )
            : search_type(search_type),
              search_str(search_str),
              priority(priority),
              speed_mod(speed_mod),
              fuel_mod(fuel_mod),
              co2_mod(co2_mod),
              fourx_mod(fourx_mod) {}
    };

    struct SearchResult {
        shared_ptr<Aircraft> ac;
        Aircraft::ParseResult parse_result;

        SearchResult(shared_ptr<Aircraft> ac, Aircraft::ParseResult parse_result)
            : ac(ac), parse_result(parse_result) {}
    };

    struct Suggestion {
        shared_ptr<Aircraft> ac;
        double score;

        Suggestion() : ac(make_shared<Aircraft>()), score(0) {}
        Suggestion(shared_ptr<Aircraft> ac, double score) : ac(ac), score(score) {}
    };

    Aircraft();
    static ParseResult parse(const string& s);
    static SearchResult search(const string& s, const User& user = User::Default());
    static std::vector<Aircraft::Suggestion> suggest(const ParseResult& parse_result);

    Aircraft(const duckdb::unique_ptr<duckdb::DataChunk>& chunk, idx_t row);
    static const string repr(const Aircraft& ac);
};

inline const string to_string(Aircraft::Type type);
inline const string to_string(Aircraft::SearchType searchtype);

#if BUILD_PYBIND == 1
#include "binder.hpp"

py::dict to_dict(const Aircraft& ac);
py::dict to_dict(const Aircraft::PaxConfig& pax_config);
py::dict to_dict(const Aircraft::CargoConfig& cargo_config);
#endif