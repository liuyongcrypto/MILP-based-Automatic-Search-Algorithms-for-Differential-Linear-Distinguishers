#include <stdio.h>
#include <math.h>
#include "Generating_random_numbers_AES.h"
#define Round 7
#define N 4194304
#define Times 100

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
	int i, j, s, t, r0;
	double cor_min = -100;
	unsigned long long OUTPUT[1][3] = { 0, 0, 0 };
	const char* pFileName = "gift64_dl_4_7_0.txt";
	const char* qFileName = "gift64_dl_4_7_0_clear.txt";
	FILE* pFile;
	FILE* qFile;
	fopen_s(&pFile, pFileName, "a");
	fopen_s(&qFile, qFileName, "a");

	unsigned long long IN[100][3] = { {0x100000000000, 0x8000000000}, { 0x1000000, 0x8000000 }, { 0x1000000000000000, 0x800000000 },{0x100000, 0x800}, { 0x1 , 0x80000 , 24000 },
{ 0x1 , 0x8000000 , 24000 },
{ 0x1 , 0x800000000000 , 24000 },
{ 0x1 , 0x80000000000 , 24000 },
{ 0x1 , 0x80 , 24000 },
{ 0x1 , 0x8000000000000000 , 24000 },
{ 0x2 , 0x4 , 26000 },
{ 0x1000000000002 , 0x400000 , 26000 },
{ 0x4 , 0x800 , 24000 },
{ 0x4000000000008 , 0x8000 , 24000 },
{ 0x10 , 0x100000 , 14000 },
{ 0x10 , 0x8000000000000000 , 24000 },
{ 0x100 , 0x800 , 24000 },
{ 0x100 , 0x8000000000 , 24000 },
{ 0x100 , 0x8 , 24000 },
{ 0x100 , 0x800000000 , 24000 },
{ 0x1000 , 0x80000000 , 24000 },
{ 0x20001000 , 0x4000000 , 26000 },
{ 0x8000000000001000 , 0x100000000000 , 14000 },
{ 0x8000000000001000 , 0x400000000 , 26000 },
{ 0x2000 , 0x80000000000 , 24000 },
{ 0x40002000 , 0x800000 , 24000 },
{ 0x4000 , 0x4000 , 26000 },
{ 0x8000 , 0x10000 , 14000 },
{ 0x10000 , 0x8000000000 , 24000 },
{ 0x10000 , 0x80 , 24000 },
{ 0x10000 , 0x80000000 , 24000 },
{ 0x20000 , 0x800000000000000 , 24000 },
{ 0x100000 , 0xa00 , 12000 },
{ 0x100000 , 0x200 , 16000 },
{ 0x100000 , 0x8000000000 , 24000 },
{ 0x100000 , 0x80000 , 24000 },
{ 0x100000 , 0x800 , 24000 },
{ 0x100000 , 0x800000000000000 , 24000 },
{ 0x100000 , 0x80000000 , 24000 },
{ 0x200000 , 0x800 , 24000 },
{ 0x8000400000 , 0x4000000000 , 26000 },
{ 0x1000000 , 0x8000 , 24000 },
{ 0x800000002000000 , 0x20000000000 , 16000 },
{ 0x80004000000 , 0x1000000000000000 , 14000 },
{ 0x100000004000000 , 0x1000000000000000 , 14000 },
{ 0x8000000 , 0x800000000000 , 24000 },
{ 0x10000000 , 0x8000000000000000 , 24000 },
{ 0x20000000 , 0xa00000000000000 , 12000 },
{ 0x20000000 , 0x200000000000000 , 16000 },
{ 0x20000000 , 0x800000000000000 , 24000 },
{ 0x40000000 , 0x8000000 , 24000 },
{ 0x80000000 , 0x10000 , 14000 },
{ 0x100000000 , 0x80000000000000 , 24000 },
{ 0x100000000 , 0x80 , 24000 },
{ 0x100000000 , 0x80000000000 , 24000 },
{ 0x100000000 , 0x800 , 24000 },
{ 0x200000000 , 0x8000000000000 , 24000 },
{ 0x400000000 , 0x8000000000000 , 24000 },
{ 0x8000400000000 , 0x400 , 26000 },
{ 0x800000000 , 0x2000000000000000 , 16000 },
{ 0x1000000000 , 0x8000000000000000 , 24000 },
{ 0x1000000000 , 0x80000000000000 , 24000 },
{ 0x2000000000 , 0x8 , 24000 },
{ 0x8000000000 , 0x800000000000000 , 24000 },
{ 0x10000000000 , 0x80 , 24000 },
{ 0x10000000000 , 0x800000000 , 24000 },
{ 0x10000000000 , 0x800000000000000 , 24000 },
{ 0x10000000000 , 0x8000000000 , 24000 },
{ 0x10000000000 , 0x800000 , 24000 },
{ 0x20000000000 , 0x800000 , 24000 },
{ 0x100000000000 , 0x80000 , 24000 },
{ 0x200000000000 , 0x8000000000 , 24000 },
{ 0x400000000000 , 0x80000 , 24000 },
{ 0x800000000000 , 0x800000000000000 , 24000 },
{ 0x1000000000000 , 0x8000000000 , 24000 },
{ 0x1000000000000 , 0x80000000000 , 24000 },
{ 0x2000000000000 , 0x8000000000000 , 24000 },
{ 0x10000000000000 , 0xc000000000000000 , 10000 },
{ 0x10000000000000 , 0x8000000 , 24000 },
{ 0x10000000000000 , 0x800000000000 , 24000 },
{ 0x20000000000000 , 0x8000 , 24000 },
{ 0x100000000000000 , 0x80000 , 24000 },
{ 0x100000000000000 , 0x8 , 24000 },
{ 0x100000000000000 , 0x800000000 , 24000 },
{ 0x100000000000000 , 0x8000000000000000 , 24000 },
{ 0x100000000000000 , 0x80000000000 , 24000 },
{ 0x200000000000000 , 0x8000000 , 24000 },
{ 0x1000000000000000 , 0x800000 , 24000 },
{ 0x1000000000000000 , 0x80 , 24000 },
{ 0x1000000000000000 , 0x8000 , 24000 },
{ 0x1000000000000000 , 0x800000000000000 , 24000 },
{ 0x1000000000000000 , 0x80000000000000 , 24000 },
{ 0x4000000000000000 , 0x200000000 , 16000 } };

	for (r0 = 0; r0 < 89; r0++) {
		double count_all = 0;
		int count_i = 0;

		printf("#############################################\n");
		printf("r0 = %d < 89\n", r0);

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

			if ((log(abs(count) / (N * 1.0)) / log(2)) <= -12.5) {

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
		if ((log(abs(count_all / (Times * 1.0)) / (N * 1.0)) / log(2)) - (IN[r0][2] / (1000 * 1.0)) > cor_min) {
			cor_min = (log(abs(count_all / (Times * 1.0)) / (N * 1.0)) / log(2)) - (IN[r0][2] / (1000 * 1.0));
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
