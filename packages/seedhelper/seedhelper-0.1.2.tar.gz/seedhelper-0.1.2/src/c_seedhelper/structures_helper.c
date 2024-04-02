#include <stdio.h>
#include <stdlib.h>

#include "../cubiomes/generator.h"
#include "../cubiomes/finders.h"
#include "../cubiomes/util.h"
#include "structures_helper.h"


Piece* get_elytras_positions(struct find_elytras_arguments* arguments, int *n_ships)
{
    const int structType = End_City;
    const int mc = str2mc(arguments->mc_version);
    const uint64_t seed = arguments->seed;
    const int c_x = arguments->x;
    const int c_z = arguments->z;
    const int r = arguments->r;

    const int min_regx = c_x - (r / REGION_SIZE - 1);
    const int max_regx = c_x + (r / REGION_SIZE + 1);

    const int min_regz = c_z - (r / REGION_SIZE - 1);
    const int max_regz = c_z + (r / REGION_SIZE + 1);

    Generator g;
    setupGenerator(&g, mc, 0);
    applySeed(&g, DIM_END, seed);

    SurfaceNoise sn;
    initSurfaceNoise(&sn, DIM_END, seed);

    Pos p;
    *n_ships = 0;
    int output_size = 2048;
    Piece* output = malloc(output_size * sizeof(Piece));
    if (!output) {
        printf("Not enough memory, try on a smaller region.\n");
        exit(1);
    }

    for (int regx = min_regx; regx <= max_regx; regx++) {
        for (int regz = min_regz; regz <= max_regz; regz++) {
            if (!getStructurePos(structType, mc, seed, regx, regz, &p))
                continue;

            applySeed(&g, DIM_END, seed);
            if (isViableEndCityTerrain(&g, &sn, p.x, p.z))
            {
                Piece buffer[END_CITY_PIECES_MAX];
                int n = getEndCityPieces(buffer, seed, p.x / 16, p.z / 16);
                for (int i = 0; i < n; i++) {
                    if (buffer[i].type == END_SHIP) {
                        (*n_ships)++;

                        if (*n_ships > output_size) {
                            output_size *= 2;
                            output = realloc(output, output_size * sizeof(Piece));
                        }

                        output[*n_ships - 1] = buffer[i];
                    }
                }
            }
        }
    }

    return output;
}
