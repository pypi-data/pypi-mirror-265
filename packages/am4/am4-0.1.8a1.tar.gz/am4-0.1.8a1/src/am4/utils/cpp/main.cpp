#include <fstream>
#include <sstream>
#include <vector>
#include <iostream>
#include <iomanip>
#include <chrono>

#include <ittnotify.h>

#include "include/db.hpp"
#include "include/game.hpp"
#include "include/ticket.hpp"
#include "include/demand.hpp"

#include "include/airport.hpp"
#include "include/aircraft.hpp"
#include "include/route.hpp"

#include "include/log.hpp"

using std::cerr;
using std::cout;
using std::endl;
using std::get;
using std::string;

#ifdef VERSION_INFO
string version = MACRO_STRINGIFY(VERSION_INFO);
#else
string version = "dev";
#endif

#ifdef _WIN32
#include <Windows.h>
string get_executable_path() {
    char result[MAX_PATH];
    GetModuleFileName(NULL, result, MAX_PATH);
    string::size_type pos = string(result).find_last_of("\\/");
    return string(result).substr(0, pos);
}
#else
#include <unistd.h>
#include <limits.h>
string get_executable_path() {
    char result[PATH_MAX];
    std::ignore = readlink("/proc/self/exe", result, PATH_MAX);
    string::size_type pos = string(result).find_last_of("\\/");
    return string(result).substr(0, pos);
}
#endif

// benchmark time
class Timer {
    std::chrono::high_resolution_clock::time_point start;

   public:
    Timer() { start = std::chrono::high_resolution_clock::now(); }

    void stop() {
        auto finish = std::chrono::high_resolution_clock::now();
        std::chrono::duration<double> elapsed = finish - start;
        cout << "elapsed: " << elapsed.count() * 1000 << " ms\n";
    }
};

int64_t to_int64(const TimePoint& time_point) {
    using namespace std::chrono;
    return duration_cast<microseconds>(time_point.time_since_epoch()).count();
}

int main() {
    // __itt_domain* domain = __itt_domain_create("main_domain");
    // __itt_string_handle* handle_main = __itt_string_handle_create("main_handle");
    string executable_path = get_executable_path();
    cout << "am4.utils (v" << version << "), executable_path: " << executable_path << "\n_______"
         << std::setprecision(15) << endl;

    try {
        init(executable_path);  // 1.3s
        // const auto& db = Database::Client();

        Airport ap0 = *Airport::search("SIN").ap;
        // Airport ap1 = *Airport::search("TPE").ap;
        Aircraft ac = *Aircraft::search("a32vip").ac;
        auto options = AircraftRoute::Options(AircraftRoute::Options::TPDMode::STRICT_ALLOW_MULTIPLE_AC, 2);
        // auto options = AircraftRoute::Options(AircraftRoute::Options::TPDMode::AUTO);
        User user = User::Default();

        auto timer = Timer();
        // __itt_task_begin(domain, __itt_null, __itt_null, handle_main);
        // auto r = AircraftRoute::create(ap0, ap1, ac, options, user);
        // auto c = std::get<Aircraft::PaxConfig>(r.config);
        // cout << "cfg: " << c.y << "," << c.j << "," << c.f << " | " << c.valid << endl;
        // auto d = r.route.pax_demand;
        // cout << "dem: " << d.y << "," << d.j << "," << d.f << endl;
        // cout << "tpd: " << r.trips_per_day_per_ac << endl;
        auto rs = RoutesSearch(ap0, ac, options, user);
        auto results = rs.get();
        std::cout << "results.size(): " << results.size() << std::endl;
        // __itt_task_end(domain);
        timer.stop();
        // getchar();

    } catch (DatabaseException& e) {
        cerr << "DatabaseException: " << e.what() << endl;
        return 1;
    }
    return 0;
}