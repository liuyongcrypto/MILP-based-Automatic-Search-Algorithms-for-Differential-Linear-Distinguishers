#include <stdio.h>
#include <math.h>
#include "Generating_random_numbers_AES.h"
#define Round 6
#define N 4194304*2
#define Times 5

unsigned long long* key_schedule(unsigned long long k[2]) {
	unsigned long long r;
	unsigned long long temp0, temp1, temp2, temp3;
	static unsigned long long rk[29] = { 0, };
	unsigned long long S[16] = { 0xc, 0x5, 0x6, 0xb, 0x9, 0x0, 0xa, 0xd, 0x3, 0xe, 0xf, 0x8, 0x4, 0x7, 0x1, 0x2 };

	temp0 = k[0];
	temp1 = k[1];
	rk[0] = (temp1 & 0xffffffff);

	for (r = 1; r < 29; r++) {
		temp2 = (((temp1 >> 16) & 0x3) << 62) ^ (((temp1 >> 18) & 0x3fff) << 48) ^ (((temp1 >> 12) & 0xf) << 32) ^ ((temp1 & 0xfff) << 36) ^ ((temp0 >> 32) & 0xffffffff);
		temp3 = ((temp0 & 0xffffffff) << 32) ^ ((temp1 >> 32) & 0xffffffff);

		temp0 = temp2;
		temp1 = temp3;

		rk[r] = (temp1 & 0xffffffff);
	}
	return rk;
}

unsigned long long gift64_enc(unsigned long long pt, unsigned long long rk[29]) {
	int r, s;
	unsigned long long ct = 0;
	unsigned long long x = pt;
	unsigned long long S[16] = { 0x1, 0xa, 0x4, 0xc, 0x6, 0xf, 0x3, 0x9, 0x2, 0xd, 0xb, 0x7, 0x5, 0x0, 0x8, 0xe };
	int P[64] = { 0, 17, 34, 51, 48, 1, 18, 35, 32, 49, 2, 19, 16, 33, 50, 3, 4, 21, 38, 55, 52, 5, 22, 39, 36, 53, 6, 23, 20, 37, 54, 7, 8, 25, 42, 59, 56, 9, 26, 43, 40, 57, 10, 27, 24, 41, 58, 11, 12, 29, 46, 63, 60, 13, 30, 47, 44, 61, 14, 31, 28, 45, 62, 15 };
	int RC[48] = { 0X01, 0X03, 0X07, 0X0F, 0X1F, 0X3E, 0X3D, 0X3B, 0X37, 0X2F, 0X1E, 0X3C, 0X39, 0X33, 0X27, 0X0E, 0X1D, 0X3A, 0X35, 0X2B, 0X16, 0X2C, 0X18, 0X30, 0X21, 0X02, 0X05, 0X0B, 0X17, 0X2E, 0X1C, 0X38, 0X31, 0X23, 0X06, 0X0D, 0X1B, 0X36, 0X2D, 0X1A, 0X34, 0X29, 0X12, 0X24, 0X08, 0X11, 0X22, 0X04 };
	unsigned long long temp0 = 0, temp1 = 0;

	for (r = 0; r < Round; r++) {
		temp0 = 0;
		temp1 = 0;

		for (s = 0; s < 16; s++) {
			temp0 = temp0 ^ (static_cast<unsigned long long>(S[(x >> (4 * s)) & 0xf]) << (4 * s));
		}
		for (s = 0; s < 64; s++) {
			temp1 = temp1 ^ (((temp0 >> s) & 0x1) << P[s]);
		}
		temp1 = temp1 ^ ((unsigned long long)1 << 63);
		temp1 = temp1 ^ ((unsigned long long)((RC[r] >> 5) & 0x1) << 23);
		temp1 = temp1 ^ ((unsigned long long)((RC[r] >> 4) & 0x1) << 19);
		temp1 = temp1 ^ ((unsigned long long)((RC[r] >> 3) & 0x1) << 15);
		temp1 = temp1 ^ ((unsigned long long)((RC[r] >> 2) & 0x1) << 11);
		temp1 = temp1 ^ ((unsigned long long)((RC[r] >> 1) & 0x1) << 7);
		temp1 = temp1 ^ ((unsigned long long)(RC[r] & 0x1) << 3);

		x = temp1;

		for (s = 0; s < 16; s++) {
			x = x ^ (((rk[r] >> s) & 0x1) << (4 * s)) ^ (((rk[r] >> (16 + s)) & 0x1) << (4 * s + 1));
		}
	}

	ct = x;
	return ct;
}

int differential_linear_verify()
{
	int i, j, s, t, r0, r1;
	double count_all = 0;
	const char* pFileName = "gift64_dl_6.txt";
	FILE* pFile;
	fopen_s(&pFile, pFileName, "a");
	unsigned long long IN[160][3] = { {0, 0, 2},{0, 17, 1},{0, 34, 2},{0, 51, 3},{1, 1, 2},{1, 18, 2},{1, 35, 3},{1, 48, 1},{2, 2, 2},{2, 19, 3},{2, 32, 2},{2, 49, 2},{3, 3, 3},{3, 16, 3},{3, 33, 3},{3, 50, 3},{4, 4, 2},{4, 21, 1},{4, 38, 2},{4, 55, 3},{5, 5, 2},{5, 22, 2},{5, 39, 3},{5, 52, 1},{6, 6, 2},{6, 23, 3},{6, 36, 2},{6, 53, 2},{7, 7, 3},{7, 20, 3},{7, 37, 3},{7, 54, 3},{8, 8, 2},{8, 25, 1},{8, 42, 2},{8, 59, 3},{9, 9, 2},{9, 26, 2},{9, 43, 3},{9, 56, 1},{10, 10, 2},{10, 27, 3},{10, 40, 2},{10, 57, 2},{11, 11, 3},{11, 24, 3},{11, 41, 3},{11, 58, 3},{12, 12, 2},{12, 29, 1},{12, 46, 2},{12, 63, 3},{13, 13, 2},{13, 30, 2},{13, 47, 3},{13, 60, 1},{14, 14, 2},{14, 31, 3},{14, 44, 2},{14, 61, 2},{15, 15, 3},{15, 28, 3},{15, 45, 3},{15, 62, 3},{16, 16, 2},{16, 33, 1},{16, 50, 2},{17, 17, 2},{17, 34, 2},{17, 51, 3},{18, 18, 2},{18, 35, 3},{18, 48, 2},{19, 19, 3},{19, 32, 3},{19, 49, 3},{20, 20, 2},{20, 37, 1},{20, 54, 2},{21, 21, 2},{21, 38, 2},{21, 55, 3},{22, 22, 2},{22, 39, 3},{22, 52, 2},{23, 23, 3},{23, 36, 3},{23, 53, 3},{24, 24, 2},{24, 41, 1},{24, 58, 2},{25, 25, 2},{25, 42, 2},{25, 59, 3},{26, 26, 2},{26, 43, 3},{26, 56, 2},{27, 27, 3},{27, 40, 3},{27, 57, 3},{28, 28, 2},{28, 45, 1},{28, 62, 2},{29, 29, 2},{29, 46, 2},{29, 63, 3},{30, 30, 2},{30, 47, 3},{30, 60, 2},{31, 31, 3},{31, 44, 3},{31, 61, 3},{32, 32, 2},{32, 49, 1},{33, 33, 2},{33, 50, 2},{34, 34, 2},{34, 51, 3},{35, 35, 3},{35, 48, 3},{36, 36, 2},{36, 53, 1},{37, 37, 2},{37, 54, 2},{38, 38, 2},{38, 55, 3},{39, 39, 3},{39, 52, 3},{40, 40, 2},{40, 57, 1},{41, 41, 2},{41, 58, 2},{42, 42, 2},{42, 59, 3},{43, 43, 3},{43, 56, 3},{44, 44, 2},{44, 61, 1},{45, 45, 2},{45, 62, 2},{46, 46, 2},{46, 63, 3},{47, 47, 3},{47, 60, 3},{48, 48, 2},{49, 49, 2},{50, 50, 2},{51, 51, 3},{52, 52, 2},{53, 53, 2},{54, 54, 2},{55, 55, 3},{56, 56, 2},{57, 57, 2},{58, 58, 2},{59, 59, 3},{60, 60, 2},{61, 61, 2},{62, 62, 2},{63, 63, 3} };

	for (r0 = 0; r0 < 160; r0++) {
		for (r1 = 0; r1 < 64; r1++) {
			printf("#############################################\n");
			printf("r0 = %d < 160, r1 = %d < 64\n", r0, r1);

			unsigned long long diff_in;
			if (IN[r0][0] == IN[r0][1]) {
				diff_in = ((unsigned long long) 1 << IN[r0][0]);
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

					unsigned long long ct_0 = gift64_enc(pt_0, rk);
					unsigned long long ct_1 = gift64_enc(pt_1, rk);
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

				if ((log(abs(count) / (N * 1.0)) / log(2)) <= -11.5) {
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
	////unsigned long long pt = 0xA231FC9B8214DE60;
	////unsigned long long k[2] = { 0x2B7E151628AED2A6, 0xABF7158809CF4F3C };
	////75da7ad18486b998
	//unsigned long long pt = 0x980ba5471ed79a08;
	//unsigned long long k[2] = { 0x6609bc34ad74ff3f, 0x21abde347681cbea };
	////9a46b202ea814fa0
	//static unsigned long long * rk = key_schedule(k);

	//unsigned long long ct = gift64_enc(pt, rk);
	//printf("%016llx \n", ct);
	

	//differential_verify();

	//linear_verify();

	differential_linear_verify();

	return 0;
}
