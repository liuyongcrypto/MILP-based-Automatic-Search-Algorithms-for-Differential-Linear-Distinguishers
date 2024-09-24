#include <stdio.h>
#include <math.h>
#include "Generating_random_numbers_AES.h"
#define Round 10
#define N 4194304*4
#define Times 5

unsigned long long* key_schedule(unsigned long long k[2]){
	unsigned long long r;
	unsigned long long temp0, temp1;
	static unsigned long long rk[32] = { 0, };
	unsigned long long S[16] = { 0xc, 0x5, 0x6, 0xb, 0x9, 0x0, 0xa, 0xd, 0x3, 0xe, 0xf, 0x8, 0x4, 0x7, 0x1, 0x2 };

	rk[0] = (k[1] << 48) ^ (k[0] & 0xffffffffffff);

	for (r = 1; r < 32; r++) {
		temp0 = ((k[0] >> 19) & 0x1fffffffffff) ^ ((k[1] & 0xffff) << 45) ^ ((k[0] & 0x7) << 61);
		temp1 = (k[0] >> 3) & 0xffff;

		k[1] = (temp1 & 0xfff) ^ (S[(temp1 >> 12) & 0xf] << 12);
		k[0] = temp0 ^ (r << 15);

		rk[r] = (k[1] << 48) ^ ((k[0]>>16) & 0xffffffffffff);
	}
	return rk;
}

unsigned long long present80_enc(unsigned long long pt, unsigned long long rk[32]){
	int r, s;
	unsigned long long ct = 0;
	unsigned long long x = pt;
	unsigned long long S[16] = { 0xc, 0x5, 0x6, 0xb, 0x9, 0x0, 0xa, 0xd, 0x3, 0xe, 0xf, 0x8, 0x4, 0x7, 0x1, 0x2 };
	int P[64] = {0, 16, 32, 48, 1, 17, 33, 49, 2, 18, 34, 50, 3, 19, 35, 51, 4, 20, 36, 52, 5, 21, 37, 53, 6, 22, 38, 54, 7, 23, 39, 55, 8, 24, 40, 56, 9, 25, 41, 57, 10, 26, 42, 58, 11, 27, 43, 59, 12, 28, 44, 60, 13, 29, 45, 61, 14, 30, 46, 62, 15, 31, 47, 63};
	unsigned long long temp0 = 0, temp1 = 0;

	for (r = 0; r < Round; r++) {
		temp0 = 0;
		temp1 = 0;
		x = x ^ rk[r];
		for (s = 0; s < 16; s++) {
			temp0 = temp0 ^ (static_cast<unsigned long long>(S[(x >> (4 * s)) & 0xf]) << (4 * s));
		}
		for (s = 0; s < 64; s++) {
			temp1 = temp1 ^ (((temp0 >> s) & 0x1) << P[s]);
		}
		x = temp1;
	}
	x = x ^ rk[Round];

	ct = x;
	return ct;
}

int differential_linear_verify()
{
	int i, j, s, t, r0, r1;
	double count_all = 0;
	const char* pFileName = "present_dl_8.txt";
	FILE* pFile;
	fopen_s(&pFile, pFileName, "a");

	unsigned long long IN[160][3] = { {0, 0, 2}, {0, 16, 2}, {0, 32, 2}, {0, 48, 2}, {1, 1, 2}, {1, 17, 2}, {1, 33, 2}, {1, 49, 2}, {2, 2, 2}, {2, 18, 2}, {2, 34, 2}, {2, 50, 2}, {3, 3, 2}, {3, 19, 2}, {3, 35, 2}, {3, 51, 2}, {4, 4, 2}, {4, 20, 2}, {4, 36, 2}, {4, 52, 2}, {5, 5, 2}, {5, 21, 2}, {5, 37, 2}, {5, 53, 2}, {6, 6, 2}, {6, 22, 2}, {6, 38, 2}, {6, 54, 2}, {7, 7, 2}, {7, 23, 2}, {7, 39, 2}, {7, 55, 2}, {8, 8, 2}, {8, 24, 2}, {8, 40, 2}, {8, 56, 2}, {9, 9, 2}, {9, 25, 2}, {9, 41, 2}, {9, 57, 2}, {10, 10, 2}, {10, 26, 2}, {10, 42, 2}, {10, 58, 2}, {11, 11, 2}, {11, 27, 2}, {11, 43, 2}, {11, 59, 2}, {12, 12, 2}, {12, 28, 2}, {12, 44, 2}, {12, 60, 2}, {13, 13, 2}, {13, 29, 2}, {13, 45, 2}, {13, 61, 2}, {14, 14, 2}, {14, 30, 2}, {14, 46, 2}, {14, 62, 2}, {15, 15, 2}, {15, 31, 2}, {15, 47, 2}, {15, 63, 2}, {16, 16, 2}, {16, 32, 2}, {16, 48, 3}, {17, 17, 2}, {17, 33, 2}, {17, 49, 3}, {18, 18, 2}, {18, 34, 2}, {18, 50, 3}, {19, 19, 2}, {19, 35, 2}, {19, 51, 3}, {20, 20, 2}, {20, 36, 2}, {20, 52, 3}, {21, 21, 2}, {21, 37, 2}, {21, 53, 3}, {22, 22, 2}, {22, 38, 2}, {22, 54, 3}, {23, 23, 2}, {23, 39, 2}, {23, 55, 3}, {24, 24, 2}, {24, 40, 2}, {24, 56, 3}, {25, 25, 2}, {25, 41, 2}, {25, 57, 3}, {26, 26, 2}, {26, 42, 2}, {26, 58, 3}, {27, 27, 2}, {27, 43, 2}, {27, 59, 3}, {28, 28, 2}, {28, 44, 2}, {28, 60, 3}, {29, 29, 2}, {29, 45, 2}, {29, 61, 3}, {30, 30, 2}, {30, 46, 2}, {30, 62, 3}, {31, 31, 2}, {31, 47, 2}, {31, 63, 3}, {32, 32, 2}, {32, 48, 2}, {33, 33, 2}, {33, 49, 2}, {34, 34, 2}, {34, 50, 2}, {35, 35, 2}, {35, 51, 2}, {36, 36, 2}, {36, 52, 2}, {37, 37, 2}, {37, 53, 2}, {38, 38, 2}, {38, 54, 2}, {39, 39, 2}, {39, 55, 2}, {40, 40, 2}, {40, 56, 2}, {41, 41, 2}, {41, 57, 2}, {42, 42, 2}, {42, 58, 2}, {43, 43, 2}, {43, 59, 2}, {44, 44, 2}, {44, 60, 2}, {45, 45, 2}, {45, 61, 2}, {46, 46, 2}, {46, 62, 2}, {47, 47, 2}, {47, 63, 2}, {48, 48, 2}, {49, 49, 2}, {50, 50, 2}, {51, 51, 2}, {52, 52, 2}, {53, 53, 2}, {54, 54, 2}, {55, 55, 2}, {56, 56, 2}, {57, 57, 2}, {58, 58, 2}, {59, 59, 2}, {60, 60, 2}, {61, 61, 2}, {62, 62, 2}, {63, 63, 2} };

	for (r0 = 0; r0 < 160; r0++) {
		for (r1 = 0; r1 < 64; r1++) {
			printf("#############################################\n");
			printf("r0 = %d < 160, r1 = %d < 64\n", r0, r1);
			unsigned long long diff_in;
			if (IN[r0][0] == IN[r0][1]) {
				diff_in = (unsigned long long) 1 << IN[r0][0];
			}
			else {
				diff_in = ((unsigned long long) 1 << IN[r0][0]) ^ ((unsigned long long) 1 << IN[r0][1]);
			}
			unsigned long long mask_out = (unsigned long long) 1 << r1;

			printf("#############################################\n");
			fprintf(pFile, "#############################################\n");

			printf("The number of rounds is %d:\n", Round);
			fprintf(pFile, "The number of rounds is %d:\n", Round);

			printf("The input difference  The output mask \n");
			fprintf(pFile, "The input difference is: The output mask is:\n");

			printf("[0x%016llx, 0x%016llx]\n", diff_in, mask_out);
			fprintf(pFile, "[0x%016llx, 0x%016llx]\n", diff_in, mask_out);

			int count_i = 0;
			for (i = 0; i < Times; i++)
			{
				unsigned long long K0 = GenerateRandomValue();
				unsigned long long K1 = GenerateRandomValue();
				unsigned long long k[2] = { K1 & 0xffff, K0 & 0xffffffffffffffff };
				static unsigned long long* rk = key_schedule(k);
				long long count = 0;

				for (j = 0; j < N; j++)
				{
					unsigned long long PT = GenerateRandomValue();
					unsigned long long pt_0 = PT & 0xffffffffffffffff;
					unsigned long long pt_1 = (unsigned long long)(pt_0 ^ diff_in);

					unsigned long long ct_0 = present80_enc(pt_0, rk);
					unsigned long long ct_1 = present80_enc(pt_1, rk);
					unsigned long long CT_0 = ct_0;
					unsigned long long CT_1 = ct_1;
					unsigned long long CT = ct_0 ^ ct_1;

					t = 0;

					for (s = 0; s < 64; s++)
					{
						t = t ^ (((mask_out & CT) >> s) & 0x1);
					}

					if (t == 0)
					{
						count = count + 1;
					}
					else
					{
						count = count - 1;
					}
				}

				if ((log(abs(count) / (N * 1.0)) / log(2)) <= -12) {
					break;
				}
				else {
					count_i = count_i + 1;
				}

				count_all += count;

				if (i == 0)
				{
					printf("The linear probability for the %d-st experiment is %lf \n", i + 1, log(abs(count) / (N * 1.0)) / log(2));
					fprintf(pFile, "The linear probability for the %d-st experiment is %lf \n", i + 1, log(abs(count) / (N * 1.0)) / log(2));
				}

				if (i == 1)
				{
					printf("The linear probability for the %d-nd experiment is %lf \n", i + 1, log(abs(count) / (N * 1.0)) / log(2));
					fprintf(pFile, "The linear probability for the %d-nd experiment is %lf \n", i + 1, log(abs(count) / (N * 1.0)) / log(2));
					}

				if (i == 2)
				{
					printf("The linear probability for the %d-rd experiment is %lf \n", i + 1, log(abs(count) / (N * 1.0)) / log(2));
					fprintf(pFile, "The linear probability for the %d-rd experiment is %lf \n", i + 1, log(abs(count) / (N * 1.0)) / log(2));
				}

				if (i >= 3)
				{
					printf("The linear probability for the %d-th experiment is %lf \n", i + 1, log(abs(count) / (N * 1.0)) / log(2));
					fprintf(pFile, "The linear probability for the %d-th experiment is %lf \n", i + 1, log(abs(count) / (N * 1.0)) / log(2));
				}
			}

			if (count_i == 3) 
			{
				printf("The average probability of 100 experiments is %lf \n", (log(abs(count_all / 3) / (N * 1.0)) / log(2)));
				fprintf(pFile, "The average probability of 100 experiments is %lf \n", (log(abs(count_all / 3) / (N * 1.0)) / log(2)));
			}
		}
	}
return 0;
}



int main() {

	/*
	unsigned long long pt = 0x0;
	unsigned long long k[2] = { 0x0, 0x0 };
	static unsigned long long * rk = key_schedule(k);
	
	unsigned long long ct = present80_enc(pt, rk);
	printf("%016llx \n", ct);
	*/

	//differential_verify();

	//linear_verify();

	differential_linear_verify();

	return 0;
}
