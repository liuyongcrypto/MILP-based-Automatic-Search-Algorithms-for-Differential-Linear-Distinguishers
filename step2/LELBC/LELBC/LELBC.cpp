#include <stdio.h>
#include <math.h>
#include "Generating_random_numbers_AES.h"
#define Round 3
#define N 4194304*8
#define Times 5

unsigned long long * key_schedule(unsigned long long k[4])
{
	int r;
	unsigned long long temp0, temp1;
	unsigned long long rk[32] = { 0, };
	unsigned int S[16] = {0xc, 0xe, 0x6, 0xa, 0x4, 0xf, 0x2, 0x7, 0x9, 0x8, 0x3, 0xb, 0x0, 0xd, 0x1, 0x5};

	for (r = 0; r < 16; r++) {
		k[3] = (((k[3] & 0xfffffff0) ^ S[k[3] & 0xf]) & 0xffffffff);

		k[3] = ((k[3] ^ ((r << 3) & 0x78)) & 0xffffffff);

		temp0 = k[0];
		temp1 = k[1];
		k[0] = k[2];
		k[1] = k[3];
		k[2] = temp0;
		k[3] = temp1;

		rk[2 * r] = ((((k[0] << 32) & 0xffffffff00000000) ^ (k[1] & 0xffffffff)) & 0xffffffffffffffff);
		rk[2 * r + 1] = ((((k[2] << 32) & 0xffffffff00000000) ^ (k[3] & 0xffffffff)) & 0xffffffffffffffff);

		rk[2 * r] = (((rk[2 * r] << 9) ^ ((rk[2 * r] >> 55) & 0x1ff)) & 0xffffffffffffffff);
		rk[2 * r + 1] = (((rk[2 * r + 1] << 15) ^ ((rk[2 * r + 1] >> 49) & 0x7fff)) & 0xffffffffffffffff);

		k[0] = ((rk[2 * r + 0] >> 32) & 0xffffffff);
		k[1] = (rk[2 * r + 0] & 0xffffffff);
		k[2] = ((rk[2 * r + 1] >> 32) & 0xffffffff);
		k[3] = (rk[2 * r + 1] & 0xffffffff);
	}
	return rk;
}

unsigned long long * lelbc_enc(unsigned long long pt[2], unsigned long long rk[32])
{
	int r, s;
	
	unsigned long long ct[2] = { 0, 0 };
	unsigned long long x[2] = { pt[0], pt[1] };
	unsigned int S[16] = { 0xc, 0xe, 0x6, 0xa, 0x4, 0xf, 0x2, 0x7, 0x9, 0x8, 0x3, 0xb, 0x0, 0xd, 0x1, 0x5 };
	unsigned long long temp0 = 0, temp1 = 0, temp2 = 0, temp3 = 0;

	for (r = 0; r < Round; r++) {
		temp0 = 0; 
		temp1 = 0; 
		temp2 = 0; 
		temp3 = 0;

		x[0] = ((x[0] ^ ((rk[2 * r] >> 32) & 0xffffffff)) & 0xffffffff);
		temp0 = (((x[0] << 5) ^ ((x[0] >> 27) & 0x1f)) & 0xffffffff);
		x[1] = x[1] ^ temp0;

		for (s = 0; s < 8; s++) {
			temp1 = temp1 ^ (static_cast<unsigned long long>(S[(x[0] >> (4 * s)) & 0xf]) << (4 * s));
			temp2 = temp2 ^ (static_cast<unsigned long long>(S[(x[1] >> (4 * s)) & 0xf]) << (4 * s));
		}

		temp3 = (((temp2 << 5) ^ ((temp2 >> 27) & 0x1f)) & 0xffffffff);
		x[0] = temp1 ^ temp3;
		x[1] = temp2 ^ (rk[2 * r] & 0xffffffff);
	}
	
	ct[0] = x[1];
	ct[1] = x[0];

	return ct;
}

int differential_verify()
{
	int i, j;
	double count_all = 0;
	const char *pFileName = "Answer_d.txt";
	FILE * pFile;
	fopen_s(&pFile, pFileName, "a");

	//int Round = 1;
	unsigned long long diff_in[2] = { 0x02000000, 0x40800000 };
	unsigned long long diff_out[2] = { 0x10000000, 0x00800000 };

	printf("#############################################\n");
	fprintf(pFile, "#############################################\n");

	printf("The number of rounds is %d:\n", Round);
	fprintf(pFile, "The number of rounds is %d:\n", Round);

	printf("The input difference is:\n");
	fprintf(pFile, "The input difference is:\n");
	for (i = 0; i < 2; i++)
	{
		printf("0x%08llx ", diff_in[i]);
		fprintf(pFile, "0x%08llx ", diff_in[i]);
	}
	printf("\n");
	fprintf(pFile, "\n");

	printf("The output difference is:\n");
	fprintf(pFile, "The output difference is:\n");

	for (i = 0; i < 2; i++)
	{
		printf("0x%08llx ", diff_out[i]);
		fprintf(pFile, "0x%08llx ", diff_out[i]);
	}
	printf("\n");
	fprintf(pFile, "\n");

	for (i = 0; i < 100; i++)
	{
		unsigned long long count = 0;

		for (j = 0; j < N; j++)
		{
			unsigned long long K0 = GenerateRandomValue();
			unsigned long long K1 = GenerateRandomValue();
			unsigned long long k[4] = { (K0 >> 32) & 0xffffffff, (K0 >> 0) & 0xffffffff, (K1 >> 32) & 0xffffffff,  (K1 >> 0) & 0xffffffff };
			unsigned long long * rk = key_schedule(k);

			unsigned long long PT_0 = GenerateRandomValue();

			unsigned long long pt_0[2] = { (PT_0 >> 32) & 0xffffffff,  (PT_0 >> 0) & 0xffffffff };
			unsigned long long pt_1[2] = { (unsigned long long)(pt_0[0] ^ diff_in[0]), (unsigned long long)(pt_0[1] ^ diff_in[1]) };

			unsigned long long * ct_0 = lelbc_enc(pt_0, rk);
			unsigned long long CT_0[2] = { ct_0[0], ct_0[1] };

			unsigned long long * ct_1 = lelbc_enc(pt_1, rk);
			unsigned long long CT_1[2] = { ct_1[0], ct_1[1] };

			if (((CT_0[0] ^ CT_1[0]) == diff_out[1]) && ((CT_0[1] ^ CT_1[1]) == diff_out[0]))
			{
				count = count + 1;
			}
		}
		count_all += log(count / 32768.0) / log(2);
		if (i == 0)
		{
			printf("The differential probability for the %d-st experiment is %lf\n", i + 1, log(count / (N * 1.0)) / log(2));
			fprintf(pFile, "The differential probability for the %d-st experiment is %lf\n", i + 1, log(count / (N * 1.0)) / log(2));
		}

		if (i == 1)
		{
			printf("The differential probability for the %d-nd experiment is %lf\n", i + 1, log(count / (N * 1.0)) / log(2));
			fprintf(pFile, "The differential probability for the %d-nd experiment is %lf\n", i + 1, log(count / (N * 1.0)) / log(2));
		}

		if (i == 2)
		{
			printf("The differential probability for the %d-rd experiment is %lf\n", i + 1, log(count / (N * 1.0)) / log(2));
			fprintf(pFile, "The differential probability for the %d-rd experiment is %lf\n", i + 1, log(count / (N * 1.0)) / log(2));
		}

		if (i >= 3)
		{
			printf("The differential probability for the %d-th experiment is %lf\n", i + 1, log(count / (N * 1.0)) / log(2));
			fprintf(pFile, "The differential probability for the %d-th experiment is %lf\n", i + 1, log(count / (N * 1.0)) / log(2));
		}

	}
	printf("The average probability of 100 experiments is %lf\n", count_all / 100);
	fprintf(pFile, "The average probability of 100 experiments is %lf\n", count_all / 100);

	return 0;
}

int linear_verify()
{
	int i, j, s, t;
	double count_all = 0;
	const char *pFileName = "Answer_l.txt";
	FILE * pFile;
	fopen_s(&pFile, pFileName, "a");

	unsigned long long mask_in[2] = { 0x40000000, 0x00000000 };
	unsigned long long mask_out[2] = { 0x80000200, 0x0C080010 };

	printf("#############################################\n");
	fprintf(pFile, "#############################################\n");

	printf("The number of rounds is %d:\n", Round);
	fprintf(pFile, "The number of rounds is %d:\n", Round);

	printf("The input mask is:\n");
	fprintf(pFile, "The input mask is:\n");
	for (i = 0; i < 2; i++)
	{
		printf("0x%08llx ", mask_in[i]);
		fprintf(pFile, "0x%08llx ", mask_in[i]);
	}
	printf("\n");
	fprintf(pFile, "\n");

	printf("The output mask is:\n");
	fprintf(pFile, "The output mask is:\n");

	for (i = 0; i < 2; i++)
	{
		printf("0x%08llx ", mask_out[i]);
		fprintf(pFile, "0x%08llx ", mask_out[i]);
	}
	printf("\n");
	fprintf(pFile, "\n");

	for (i = 0; i < 100; i++)
	{
		unsigned long long K0 = GenerateRandomValue();
		unsigned long long K1 = GenerateRandomValue();
		unsigned long long k[4] = { (K0 >> 32) & 0xffffffff, (K0 >> 0) & 0xffffffff, (K1 >> 32) & 0xffffffff,  (K1 >> 0) & 0xffffffff };
		unsigned long long * rk = key_schedule(k);

		long long count = 0;

		for (j = 0; j < N; j++)
		{
			unsigned long long PT = GenerateRandomValue();
			unsigned long long pt[2] = { (PT >> 32) & 0xffffffff,  (PT >> 0) & 0xffffffff };
			
			unsigned long long * ct = lelbc_enc(pt, rk);
			unsigned long long CT[2] = { ct[0], ct[1] };

			t = 0;

			for (s = 0; s < 32; s++)
			{
				t = t ^ (((mask_in[0] & pt[0]) >> s) & 0x1);
			}
			for (s = 0; s < 32; s++)
			{
				t = t ^ (((mask_in[1] & pt[1]) >> s) & 0x1);
			}
			for (s = 0; s < 32; s++)
			{
				t = t ^ (((mask_out[0] & CT[1]) >> s) & 0x1);
			}
			for (s = 0; s < 32; s++)
			{
				t = t ^ (((mask_out[1] & CT[0]) >> s) & 0x1);
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

		count_all += count;

		if (i == 0)
		{
			printf("The linear probability for the %d-st experiment is %lf\n", i + 1, log(abs(count) / (N * 1.0)) / log(2));
			fprintf(pFile, "The linear probability for the %d-st experiment is %lf\n", i + 1, log(abs(count) / (N * 1.0)) / log(2));
		}

		if (i == 1)
		{
			printf("The linear probability for the %d-nd experiment is %lf\n", i + 1, log(abs(count) / (N * 1.0)) / log(2));
			fprintf(pFile, "The linear probability for the %d-nd experiment is %lf\n", i + 1, log(abs(count) / (N * 1.0)) / log(2));
		}

		if (i == 2)
		{
			printf("The linear probability for the %d-rd experiment is %lf\n", i + 1, log(abs(count) / (N * 1.0)) / log(2));
			fprintf(pFile, "The linear probability for the %d-rd experiment is %lf\n", i + 1, log(abs(count) / (N * 1.0)) / log(2));
		}

		if (i >= 3)
		{
			printf("The linear probability for the %d-th experiment is %lf\n", i + 1, log(abs(count) / (N * 1.0)) / log(2));
			fprintf(pFile, "The linear probability for the %d-th experiment is %lf\n", i + 1, log(abs(count) / (N * 1.0)) / log(2));
		}

	}

	printf("The average probability of 100 experiments is %lf\n", log(abs(count_all / 100) / (N * 1.0)) / log(2));
	fprintf(pFile, "The average probability of 100 experiments is %lf\n", log(abs(count_all / 100) / (N * 1.0)) / log(2));

	return 0;
}

int differential_linear_verify()
{
	int i, j, s, t, r0, r1;
	double count_all = 0;
	const char* pFileName = "lelbc_dl_3.txt";
	FILE* pFile;
	fopen_s(&pFile, pFileName, "a");

	unsigned long long IN[112][3] = { {0, 37, 3}, {1, 38, 2}, {2, 39, 3}, {3, 40, 2}, {4, 41, 3}, {5, 42, 2}, {6, 43, 3}, {7, 44, 2}, {8, 45, 3}, {9, 46, 2}, {10, 47, 3}, {11, 48, 2}, {12, 49, 3}, {13, 50, 2}, {14, 51, 3}, {15, 52, 2}, {16, 53, 3}, {17, 54, 2}, {18, 55, 3}, {19, 56, 2}, {20, 57, 3}, {21, 58, 2}, {22, 59, 3}, {23, 60, 2}, {24, 61, 3}, {25, 62, 2}, {26, 63, 3}, {27, 32, 2}, {28, 33, 3}, {29, 34, 2}, {30, 35, 3}, {31, 36, 2}, {32, 32, 3}, {32, 33, 3}, {32, 34, 2}, {32, 35, 2}, {33, 33, 2}, {33, 34, 3}, {33, 35, 2}, {34, 34, 3}, {34, 35, 2}, {35, 35, 2}, {36, 36, 3}, {36, 37, 3}, {36, 38, 2}, {36, 39, 2}, {37, 37, 2}, {37, 38, 3}, {37, 39, 2}, {38, 38, 3}, {38, 39, 2}, {39, 39, 2}, {40, 40, 3}, {40, 41, 3}, {40, 42, 2}, {40, 43, 2}, {41, 41, 2}, {41, 42, 3}, {41, 43, 2}, {42, 42, 3}, {42, 43, 2}, {43, 43, 2}, {44, 44, 3}, {44, 45, 3}, {44, 46, 2}, {44, 47, 2}, {45, 45, 2}, {45, 46, 3}, {45, 47, 2}, {46, 46, 3}, {46, 47, 2}, {47, 47, 2}, {48, 48, 3}, {48, 49, 3}, {48, 50, 2}, {48, 51, 2}, {49, 49, 2}, {49, 50, 3}, {49, 51, 2}, {50, 50, 3}, {50, 51, 2}, {51, 51, 2}, {52, 52, 3}, {52, 53, 3}, {52, 54, 2}, {52, 55, 2}, {53, 53, 2}, {53, 54, 3}, {53, 55, 2}, {54, 54, 3}, {54, 55, 2}, {55, 55, 2}, {56, 56, 3}, {56, 57, 3}, {56, 58, 2}, {56, 59, 2}, {57, 57, 2}, {57, 58, 3}, {57, 59, 2}, {58, 58, 3}, {58, 59, 2}, {59, 59, 2}, {60, 60, 3}, {60, 61, 3}, {60, 62, 2}, {60, 63, 2}, {61, 61, 2}, {61, 62, 3}, {61, 63, 2}, {62, 62, 3}, {62, 63, 2}, {63, 63, 2} };

	for (r0 = 0; r0 < 112; r0++){
		for (r1 = 0; r1 < 64; r1++) {
			unsigned long long diff_in[2];
			unsigned long long mask_out[2];

			if (IN[r0][0] == IN[r0][1]) {
				if (IN[r0][0] <= 31) {
					diff_in[0] = 0;
					diff_in[1] = ((unsigned long long) 1 << IN[r0][0]);
				}
				else {
					diff_in[0] = ((unsigned long long) 1 << (IN[r0][0] - 32));
					diff_in[1] = 0;
				}
			}
			else {
				if (IN[r0][0] <= 31) {
					if (IN[r0][1] <= 31) {
						diff_in[0] = 0;
						diff_in[1] = ((unsigned long long) 1 << IN[r0][0]) ^ ((unsigned long long) 1 << IN[r0][1]);
					}
					else {
						diff_in[0] = ((unsigned long long) 1 << (IN[r0][1] - 32));
						diff_in[1] = ((unsigned long long) 1 << IN[r0][0]);
					}
				}
				else {
					if (IN[r0][1] <= 31) {
						diff_in[0] = ((unsigned long long) 1 << (IN[r0][0] - 32));
						diff_in[1] = ((unsigned long long) 1 << IN[r0][1]);
					}
					else {
						diff_in[0] = ((unsigned long long) 1 << (IN[r0][0] - 32)) ^ ((unsigned long long) 1 << (IN[r0][1] - 32));
						diff_in[1] = 0;
					}
				}
			}

			if (r1 <= 31) {
				mask_out[0] = 0;
				mask_out[1] = ((unsigned long long) 1 << r1);
			}
			else {
				mask_out[0] = ((unsigned long long) 1 << (r1 - 32));
				mask_out[1] = 0;
			}

			printf("#############################################\n");
			fprintf(pFile, "#############################################\n");

			printf("The number of rounds is %d:\n", Round);
			fprintf(pFile, "The number of rounds is %d:\n", Round);

			printf("The input difference is:\n");
			fprintf(pFile, "The input difference is:\n");

			for (i = 0; i < 2; i++)
			{
				printf("0x%08llx ", diff_in[i]);
				fprintf(pFile, "0x%08llx ", diff_in[i]);
			}
			printf("\n");
			fprintf(pFile, "\n");

			printf("The output mask is:\n");
			fprintf(pFile, "The output mask is:\n");

			for (i = 0; i < 2; i++)
			{
				printf("0x%08llx ", mask_out[i]);
				fprintf(pFile, "0x%08llx ", mask_out[i]);
			}
			printf("\n");
			fprintf(pFile, "\n");

			for (i = 0; i < Times; i++)
			{
				unsigned long long K0 = GenerateRandomValue();
				unsigned long long K1 = GenerateRandomValue();
				unsigned long long k[4] = { (K0 >> 32) & 0xffffffff, (K0 >> 0) & 0xffffffff, (K1 >> 32) & 0xffffffff,  (K1 >> 0) & 0xffffffff };
				unsigned long long* rk = key_schedule(k);

				long long count = 0;

				for (j = 0; j < N; j++)
				{
					unsigned long long PT = GenerateRandomValue();
					unsigned long long pt_0[2] = { (PT >> 32) & 0xffffffff,  (PT >> 0) & 0xffffffff };
					unsigned long long pt_1[2] = { (unsigned long long)(pt_0[0] ^ diff_in[0]), (unsigned long long)(pt_0[1] ^ diff_in[1]) };

					unsigned long long* ct_0 = lelbc_enc(pt_0, rk);
					unsigned long long* ct_1 = lelbc_enc(pt_1, rk);
					unsigned long long CT_0[2] = { ct_0[0], ct_0[1] };
					unsigned long long CT_1[2] = { ct_1[0], ct_1[1] };
					unsigned long long CT[2] = { ct_0[0] ^ ct_1[0], ct_0[1] ^ ct_1[1] };

					t = 0;

					for (s = 0; s < 32; s++)
					{
						t = t ^ (((mask_out[0] & CT[1]) >> s) & 0x1);
					}
					for (s = 0; s < 32; s++)
					{
						t = t ^ (((mask_out[1] & CT[0]) >> s) & 0x1);
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

				printf("%lld\n", count);

				if ((log(abs(count) / (N * 1.0)) / log(2)) <= -12.5) {
					break;
				}

				count_all += count;

				if (i == 0)
				{
					printf("The linear probability for the %d-st experiment is %lf\n", i + 1, log(abs(count) / (N * 1.0)) / log(2));
					fprintf(pFile, "The linear probability for the %d-st experiment is %lf\n", i + 1, log(abs(count) / (N * 1.0)) / log(2));
				}

				if (i == 1)
				{
					printf("The linear probability for the %d-nd experiment is %lf\n", i + 1, log(abs(count) / (N * 1.0)) / log(2));
					fprintf(pFile, "The linear probability for the %d-nd experiment is %lf\n", i + 1, log(abs(count) / (N * 1.0)) / log(2));
				}

				if (i == 2)
				{
					printf("The linear probability for the %d-rd experiment is %lf\n", i + 1, log(abs(count) / (N * 1.0)) / log(2));
					fprintf(pFile, "The linear probability for the %d-rd experiment is %lf\n", i + 1, log(abs(count) / (N * 1.0)) / log(2));
				}

				if (i >= 3)
				{
					printf("The linear probability for the %d-th experiment is %lf\n", i + 1, log(abs(count) / (N * 1.0)) / log(2));
					fprintf(pFile, "The linear probability for the %d-th experiment is %lf\n", i + 1, log(abs(count) / (N * 1.0)) / log(2));
				}

			}

			printf("The average probability of 100 experiments is %lf\n", log(abs(count_all / 100) / (N * 1.0)) / log(2));
			fprintf(pFile, "The average probability of 100 experiments is %lf\n", log(abs(count_all / 100) / (N * 1.0)) / log(2));
		}
	}

	return 0;
}

int main() { 

	
	//unsigned long long pt_0[2] = { 0Xa44d535e, 0xfcdcac83 };
	//unsigned long long pt_1[2] = { 0x1cae22d4, 0x3ddf2c8b };
	//unsigned long long k[4] = { 0x0, 0x0, 0x0, 0x0 };
	//unsigned long long * rk = key_schedule(k);

	//unsigned long long * ct_0 = lelbc_enc(pt_0, rk);
	//unsigned long long CT_0[2] = { ct_0[0],ct_0[1] };

	//unsigned long long * ct_1 = lelbc_enc(pt_1, rk);
	//unsigned long long CT_1[2] = { ct_1[0],ct_1[1] };

	//printf("%llx %llx \n", CT_0[0], CT_0[1]);

	//printf("%llx %llx \n", CT_1[0], CT_1[1]);
	
	
	//differential_verify();

	//linear_verify();

	differential_linear_verify();

	return 0;
}
