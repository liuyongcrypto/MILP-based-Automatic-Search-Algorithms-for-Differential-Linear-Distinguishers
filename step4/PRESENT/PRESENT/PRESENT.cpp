#include <stdio.h>
#include <math.h>
#include "Generating_random_numbers_AES.h"
#define Round 8
#define N 4194304
#define Times 100

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
	int i, j, s, t, r0;
	double cor_min = -100;
	unsigned long long OUTPUT[1][3] = { 0, 0, 0 };
	const char* pFileName = "present80_dl_5_8_0.txt";
	const char* qFileName = "present80_dl_5_8_0_clear.txt";
	FILE* pFile;
	FILE* qFile;
	fopen_s(&pFile, pFileName, "a");
	fopen_s(&qFile, qFileName, "a");

	unsigned long long IN[88][3] = { {0x2,0x0080000000000000}, {0x200,0x800000}, { 0x2000000000,0x20000000,1 },
		{ 0x100000001 , 0x200000 , 27 },
{ 0x100000001 , 0x80000000000000 , 27 },
{ 0x20002 , 0x8000000000000000 , 31 },
{ 0x200000002 , 0x10000 , 27 },
{ 0x2000000000002 , 0x20000000000000 , 28 },
{ 0x4 , 0x800000000000 , 29 },
{ 0x400000004 , 0x2000000000000000 , 25 },
{ 0x4000000000004 , 0x200000 , 26 },
{ 0x1000000010 , 0x4000000000000000 , 27 },
{ 0x2000000020 , 0x8000000000000000 , 27 },
{ 0x40 , 0x10000000 , 29 },
{ 0x400040 , 0x200000 , 29 },
{ 0x4000000040 , 0x200000 , 25 },
{ 0x4000000040 , 0x20000000000 , 25 },
{ 0x4000000040 , 0x200000000000 , 25 },
{ 0x40000000000040 , 0x800 , 26 },
{ 0x800080 , 0x100 , 31 },
{ 0x8000000080 , 0x10000000000000 , 27 },
{ 0x100 , 0x800000000000 , 31 },
{ 0x100 , 0x2000000000 , 31 },
{ 0x100 , 0x80000000 , 31 },
{ 0x100 , 0x40000000000000 , 31 },
{ 0x10000000100 , 0x40000000000000 , 26 },
{ 0x200 , 0x800000000000 , 31 },
{ 0x2000200 , 0x200000 , 30 },
{ 0x20000000200 , 0x200000000000 , 26 },
{ 0x400 , 0x800000000000 , 27 },
{ 0x40000000400 , 0x20000000 , 24 },
{ 0x40000000400 , 0x2000000000000000 , 24 },
{ 0x800 , 0x8000000000000000 , 31 },
{ 0x800 , 0x80000000 , 31 },
{ 0x10001000 , 0x100000000000000 , 31 },
{ 0x1000000000001000 , 0x800000000000000 , 28 },
{ 0x4000 , 0x20000000000000 , 29 },
{ 0x4000 , 0x800000 , 29 },
{ 0x40004000 , 0x20000000 , 29 },
{ 0x400000004000 , 0x2000000000 , 25 },
{ 0x400000004000 , 0x8000000 , 25 },
{ 0x800000008000 , 0x8000000000 , 27 },
{ 0x1000000010000 , 0x40000000 , 28 },
{ 0x2000000020000 , 0x200000 , 28 },
{ 0x40000 , 0x8000000000 , 29 },
{ 0x400040000 , 0x4000000000 , 26 },
{ 0x400000 , 0x8000000000 , 29 },
{ 0x40000000400000 , 0x200000 , 26 },
{ 0x8000800000 , 0x80000000000 , 28 },
{ 0x1000000 , 0x40000000000000 , 31 },
{ 0x1000000 , 0x40000000 , 31 },
{ 0x1000000 , 0x4000000000000000 , 31 },
{ 0x1000000 , 0x800000000000000 , 31 },
{ 0x100000001000000 , 0x200000 , 27 },
{ 0x2000000 , 0x800000000000 , 31 },
{ 0x2000000 , 0x40000000000000 , 31 },
{ 0x4000000 , 0x8000000000 , 27 },
{ 0x4000000 , 0x80000000000000 , 27 },
{ 0x4000000 , 0x200000000000000 , 27 },
{ 0x8000000 , 0x400000 , 31 },
{ 0x1000000010000000 , 0x100000000 , 28 },
{ 0x40000000 , 0x8000000 , 29 },
{ 0x40000000 , 0x2000000000000000 , 29 },
{ 0x400000000 , 0x8000000000 , 28 },
{ 0x400000000 , 0x800000000000000 , 28 },
{ 0x4000000000 , 0x100000 , 28 },
{ 0x80008000000000 , 0x800000 , 28 },
{ 0x10000000000 , 0x4000000000000000 , 30 },
{ 0x20000000000 , 0x800000000000 , 30 },
{ 0x20000000000 , 0x4000000000000000 , 30 },
{ 0x40000000000 , 0x4000000000 , 26 },
{ 0x40000000000 , 0x8000000000 , 26 },
{ 0x40000000000 , 0x400000000000000 , 26 },
{ 0x80000000000 , 0x40000000000000 , 30 },
{ 0x400000000000 , 0x40000000000000 , 28 },
{ 0x4000000000000 , 0x800000000000000 , 29 },
{ 0x4000000000000 , 0x8000000 , 29 },
{ 0x40000000000000 , 0x4000000000000000 , 29 },
{ 0x40000000000000 , 0x800000000000 , 29 },
{ 0x100000000000000 , 0x400000 , 31 },
{ 0x100000000000000 , 0x80000000000000 , 31 },
{ 0x100000000000000 , 0x8000000000000000 , 31 },
{ 0x100000000000000 , 0x80000000 , 31 },
{ 0x100000000000000 , 0x4000000000000000 , 31 },
{ 0x200000000000000 , 0x8000000000 , 31 },
{ 0x400000000000000 , 0x40000000 , 27 },
{ 0x800000000000000 , 0x8000000000000000 , 31 },
{ 0x4000000000000000 , 0x800000000000 , 29 } };

	for (r0 = 0; r0 < 85; r0++) {
		double count_all = 0;
		int count_i = 0;
		printf("#############################################\n");
		printf("r0 = %d < 85 \n", 0 + r0);

		unsigned long long diff_in = IN[r0][0];

		unsigned long long mask_out = IN[r0][1];

		printf("#############################################\n");
		fprintf(pFile, "#############################################\n");
		fprintf(qFile, "#############################################\n");

		printf("The number of rounds is %d:\n", Round);
		fprintf(pFile, "The number of rounds is %d:\n", Round);
		fprintf(qFile, "The number of rounds is %d:\n", Round);

		printf("The input difference  The output mask \n");
		fprintf(pFile, "The input difference is: The output mask is:\n");
		fprintf(qFile, "The input difference is: The output mask is:\n");

		printf("[0x%016llx, 0x%016llx]\n", diff_in, mask_out);
		fprintf(pFile, "[0x%016llx, 0x%016llx]\n", diff_in, mask_out);
		fprintf(qFile, "[0x%016llx, 0x%016llx]\n", diff_in, mask_out);

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
				printf("The average correlation of 100 experiments is 0 \n");
				fprintf(pFile, "The average correlation of 100 experiments is 0 \n");
				fprintf(qFile, "The average correlation of 100 experiments is 0 \n");

				break;
			}
			else {
				count_i = count_i + 1;
			}

			count_all += count;

			if (i == 0)
			{
				printf("The linear correlation for the %d-st experiment is %lf \n", i + 1, log(abs(count) / (N * 1.0)) / log(2));
				fprintf(pFile, "The linear correlation for the %d-st experiment is %lf \n", i + 1, log(abs(count) / (N * 1.0)) / log(2));
			}

			if (i == 1)
			{
				printf("The linear correlation for the %d-nd experiment is %lf \n", i + 1, log(abs(count) / (N * 1.0)) / log(2));
				fprintf(pFile, "The linear correlation for the %d-nd experiment is %lf \n", i + 1, log(abs(count) / (N * 1.0)) / log(2));
				}

			if (i == 2)
			{
				printf("The linear correlation for the %d-rd experiment is %lf \n", i + 1, log(abs(count) / (N * 1.0)) / log(2));
				fprintf(pFile, "The linear correlation for the %d-rd experiment is %lf \n", i + 1, log(abs(count) / (N * 1.0)) / log(2));
			}

			if (i >= 3)
			{
				printf("The linear correlation for the %d-th experiment is %lf \n", i + 1, log(abs(count) / (N * 1.0)) / log(2));
				fprintf(pFile, "The linear correlation for the %d-th experiment is %lf \n", i + 1, log(abs(count) / (N * 1.0)) / log(2));
			}
		}

		if (count_i == Times)
		{
			printf("The average correlation of 100 experiments is %lf \n", (log(abs(count_all / (Times * 1.0)) / (N * 1.0)) / log(2)));
			fprintf(pFile, "The average correlation of 100 experiments is %lf \n", (log(abs(count_all / (Times * 1.0)) / (N * 1.0)) / log(2)));
			fprintf(qFile, "The average correlation of 100 experiments is %lf \n", (log(abs(count_all / (Times * 1.0)) / (N * 1.0)) / log(2)));
		}
		if ((log(abs(count_all / (Times * 1.0)) / (N * 1.0)) / log(2)) - IN[r0][2] > cor_min) {
			cor_min = (log(abs(count_all / (Times * 1.0)) / (N * 1.0)) / log(2)) - IN[r0][2];
			OUTPUT[0][0] = IN[r0][0];
			OUTPUT[0][1] = IN[r0][1];
			OUTPUT[0][2] = IN[r0][2];
		}
	}
	printf("The final input difference  The final output mask \n");
	fprintf(pFile, "The final input difference is: The final output mask is:\n");
	fprintf(qFile, "The final input difference is: The final output mask is:\n");

	printf("[0x%016llx, 0x%016llx, %lld]\n", OUTPUT[0][0], OUTPUT[0][1], OUTPUT[0][2]);
	fprintf(pFile, "[0x%016llx, 0x%016llx, %lld]\n", OUTPUT[0][0], OUTPUT[0][1], OUTPUT[0][2]);
	fprintf(qFile, "[0x%016llx, 0x%016llx, %lld]\n", OUTPUT[0][0], OUTPUT[0][1], OUTPUT[0][2]);

	printf("The final correlation is %lf \n", cor_min);
	fprintf(pFile, "The final correlation is %lf \n", cor_min);
	fprintf(qFile, "The final correlation is %lf \n", cor_min);

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
