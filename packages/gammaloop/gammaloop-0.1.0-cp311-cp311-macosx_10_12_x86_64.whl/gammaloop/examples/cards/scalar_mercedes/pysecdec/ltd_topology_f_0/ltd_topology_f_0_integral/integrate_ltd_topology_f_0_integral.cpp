#include <cstdlib> // std::atof
#include <iostream> // std::cout
#include <numeric> // std::accumulate
#include <vector> // std::vector

#include <secdecutil/integrators/cuba.hpp> // secdecutil::cuba::Vegas, secdecutil::cuba::Suave, secdecutil::cuba::Cuhre, secdecutil::cuba::Divonne
#include <secdecutil/integrators/qmc.hpp> // secdecutil::integrators::Qmc
#include <secdecutil/series.hpp> // secdecutil::Series
#include <secdecutil/uncertainties.hpp> // secdecutil::UncorrelatedDeviation
#include <secdecutil/deep_apply.hpp> // secdecutil::deep_apply

#include "ltd_topology_f_0_integral.hpp"

void print_integral_info()
{
    std::cout << "-- print_integral_info --" << std::endl;
    std::cout << "ltd_topology_f_0_integral::number_of_sectors " << ltd_topology_f_0_integral::number_of_sectors << std::endl;

    std::cout << "ltd_topology_f_0_integral::number_of_regulators " << ltd_topology_f_0_integral::number_of_regulators << std::endl;
    std::cout << "ltd_topology_f_0_integral::names_of_regulators ";
    for ( const auto& name : ltd_topology_f_0_integral::names_of_regulators )
        std::cout << " " << name;
    std::cout << std::endl;

    std::cout << "ltd_topology_f_0_integral::number_of_real_parameters " << ltd_topology_f_0_integral::number_of_real_parameters << std::endl;
    std::cout << "ltd_topology_f_0_integral::names_of_real_parameters ";
    for ( const auto& name : ltd_topology_f_0_integral::names_of_real_parameters )
        std::cout << " " << name;
    std::cout << std::endl;

    std::cout << "ltd_topology_f_0_integral::number_of_complex_parameters " << ltd_topology_f_0_integral::number_of_complex_parameters << std::endl;
    std::cout << "ltd_topology_f_0_integral::names_of_complex_parameters ";
    for ( const auto& name : ltd_topology_f_0_integral::names_of_complex_parameters )
        std::cout << " " << name;
    std::cout << std::endl;

    std::cout << "ltd_topology_f_0_integral::lowest_orders";
    for ( const auto& lowest_order : ltd_topology_f_0_integral::lowest_orders )
        std::cout << " " << lowest_order;
    std::cout << std::endl;

    std::cout << "ltd_topology_f_0_integral::highest_orders";
    for ( const auto& highest_order : ltd_topology_f_0_integral::highest_orders )
        std::cout << " " << highest_order;
    std::cout << std::endl;

    std::cout << "ltd_topology_f_0_integral::lowest_prefactor_orders";
    for ( const auto& highest_order : ltd_topology_f_0_integral::lowest_prefactor_orders )
        std::cout << " " << highest_order;
    std::cout << std::endl;

    std::cout << "ltd_topology_f_0_integral::highest_prefactor_orders";
    for ( const auto& highest_order : ltd_topology_f_0_integral::highest_prefactor_orders )
        std::cout << " " << highest_order;
    std::cout << std::endl;

    std::cout << "ltd_topology_f_0_integral::requested_orders";
    for ( const auto& requested_order : ltd_topology_f_0_integral::requested_orders )
        std::cout << " " << requested_order;
    std::cout << std::endl;
}

int main(int argc, const char *argv[])
{
    // Check the command line argument number
    if (argc != 1 + 3 + 2*0) {
        std::cout << "usage: " << argv[0];
        for ( const auto& name : ltd_topology_f_0_integral::names_of_real_parameters )
            std::cout << " " << name;
        for ( const auto& name : ltd_topology_f_0_integral::names_of_complex_parameters )
            std::cout << " re(" << name << ") im(" << name << ")";
        std::cout << std::endl;
        return 1;
    }

    std::vector<ltd_topology_f_0_integral::real_t> real_parameters; // = { real parameter values ("p11","p12","p22") go here };
    std::vector<ltd_topology_f_0_integral::complex_t> complex_parameters; // = { complex parameter values () go here };

    // Load parameters from the command line arguments
    for (int i = 1; i < 1 + 3; i++)
        real_parameters.push_back(ltd_topology_f_0_integral::real_t(std::atof(argv[i])));

    for (int i = 1 + 3; i < 1 + 3 + 2*0; i += 2) {
        ltd_topology_f_0_integral::real_t re = std::atof(argv[i]);
        ltd_topology_f_0_integral::real_t im = std::atof(argv[i+1]);
        complex_parameters.push_back(ltd_topology_f_0_integral::complex_t(re, im));
    }

    // Generate the integrands (optimisation of the contour if applicable)
    std::cerr << "Generating integrands (optimising contour if required)" << std::endl;
    const std::vector<ltd_topology_f_0_integral::nested_series_t<ltd_topology_f_0_integral::integrand_t>> sector_integrands =
        ltd_topology_f_0_integral::make_integrands(real_parameters, complex_parameters);

    // Add integrands of sectors (together flag)
    std::cerr << "Summing integrands" << std::endl;
    const ltd_topology_f_0_integral::nested_series_t<ltd_topology_f_0_integral::integrand_t> all_sectors =
        std::accumulate(++sector_integrands.begin(), sector_integrands.end(), *sector_integrands.begin());

    // Integrate
    std::cerr << "Integrating" << std::endl;
    secdecutil::cuba::Vegas<ltd_topology_f_0_integral::integrand_return_t> integrator;
    integrator.flags = 2; // verbose output --> see cuba manual
    const ltd_topology_f_0_integral::nested_series_t<secdecutil::UncorrelatedDeviation<ltd_topology_f_0_integral::integrand_return_t>> result_all =
        secdecutil::deep_apply( all_sectors, integrator.integrate );

    std::cout << "------------" << std::endl << std::endl;

    std::cout << "-- integral info -- " << std::endl;
    print_integral_info();
    std::cout << std::endl;

    std::cout << "-- integral without prefactor -- " << std::endl;
    std::cout << result_all << std::endl << std::endl;

    std::cout << "-- prefactor -- " << std::endl;
    const ltd_topology_f_0_integral::nested_series_t<ltd_topology_f_0_integral::integrand_return_t> prefactor =
        ltd_topology_f_0_integral::prefactor(real_parameters, complex_parameters);
    std::cout << prefactor << std::endl << std::endl;

    std::cout << "-- full result (prefactor*integral) -- " << std::endl;
    std::cout << prefactor*result_all << std::endl;

    return 0;
}
