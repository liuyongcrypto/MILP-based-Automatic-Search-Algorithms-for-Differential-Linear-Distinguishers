#include <stdio.h>
#include <math.h>
#include<stdint.h>
#include "Generating_random_numbers_AES.h"
#define Round 4
#define N 4194304*8
#define Times 100

void key_schedule(unsigned long long k[4], unsigned long long rk[32])
{
	int r;
	unsigned long long temp0, temp1;
	//unsigned long long rk[32] = { 0, };
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
	//return rk;
}

void lelbc_enc(unsigned long long pt[2], unsigned long long ct[2], unsigned long long rk[32])
{
	int r, s;
	
	//unsigned long long ct[2] = { 0, 0 };
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

	//return ct;
}

//int differential_verify()
//{
//	int i, j;
//	double count_all = 0;
//	const char *pFileName = "Answer_d.txt";
//	FILE * pFile;
//	fopen_s(&pFile, pFileName, "a");
//
//	//int Round = 1;
//	unsigned long long diff_in[2] = { 0x02000000, 0x40800000 };
//	unsigned long long diff_out[2] = { 0x10000000, 0x00800000 };
//
//	printf("#############################################\n");
//	fprintf(pFile, "#############################################\n");
//
//	printf("The number of rounds is %d:\n", Round);
//	fprintf(pFile, "The number of rounds is %d:\n", Round);
//
//	printf("The input difference is:\n");
//	fprintf(pFile, "The input difference is:\n");
//	for (i = 0; i < 2; i++)
//	{
//		printf("0x%08llx ", diff_in[i]);
//		fprintf(pFile, "0x%08llx ", diff_in[i]);
//	}
//	printf("\n");
//	fprintf(pFile, "\n");
//
//	printf("The output difference is:\n");
//	fprintf(pFile, "The output difference is:\n");
//
//	for (i = 0; i < 2; i++)
//	{
//		printf("0x%08llx ", diff_out[i]);
//		fprintf(pFile, "0x%08llx ", diff_out[i]);
//	}
//	printf("\n");
//	fprintf(pFile, "\n");
//
//	for (i = 0; i < 100; i++)
//	{
//		unsigned long long count = 0;
//
//		for (j = 0; j < N; j++)
//		{
//			unsigned long long K0 = GenerateRandomValue();
//			unsigned long long K1 = GenerateRandomValue();
//			unsigned long long k[4] = { (K0 >> 32) & 0xffffffff, (K0 >> 0) & 0xffffffff, (K1 >> 32) & 0xffffffff,  (K1 >> 0) & 0xffffffff };
//			unsigned long long * rk = key_schedule(k);
//
//			unsigned long long PT_0 = GenerateRandomValue();
//
//			unsigned long long pt_0[2] = { (PT_0 >> 32) & 0xffffffff,  (PT_0 >> 0) & 0xffffffff };
//			unsigned long long pt_1[2] = { (unsigned long long)(pt_0[0] ^ diff_in[0]), (unsigned long long)(pt_0[1] ^ diff_in[1]) };
//
//			unsigned long long * ct_0 = lelbc_enc(pt_0, rk);
//			unsigned long long CT_0[2] = { ct_0[0], ct_0[1] };
//
//			unsigned long long * ct_1 = lelbc_enc(pt_1, rk);
//			unsigned long long CT_1[2] = { ct_1[0], ct_1[1] };
//
//			if (((CT_0[0] ^ CT_1[0]) == diff_out[1]) && ((CT_0[1] ^ CT_1[1]) == diff_out[0]))
//			{
//				count = count + 1;
//			}
//		}
//		count_all += log(count / 32768.0) / log(2);
//		if (i == 0)
//		{
//			printf("The differential correlation for the %d-st experiment is %lf\n", i + 1, log(count / (N * 1.0)) / log(2));
//			fprintf(pFile, "The differential correlation for the %d-st experiment is %lf\n", i + 1, log(count / (N * 1.0)) / log(2));
//		}
//
//		if (i == 1)
//		{
//			printf("The differential correlation for the %d-nd experiment is %lf\n", i + 1, log(count / (N * 1.0)) / log(2));
//			fprintf(pFile, "The differential correlation for the %d-nd experiment is %lf\n", i + 1, log(count / (N * 1.0)) / log(2));
//		}
//
//		if (i == 2)
//		{
//			printf("The differential correlation for the %d-rd experiment is %lf\n", i + 1, log(count / (N * 1.0)) / log(2));
//			fprintf(pFile, "The differential correlation for the %d-rd experiment is %lf\n", i + 1, log(count / (N * 1.0)) / log(2));
//		}
//
//		if (i >= 3)
//		{
//			printf("The differential correlation for the %d-th experiment is %lf\n", i + 1, log(count / (N * 1.0)) / log(2));
//			fprintf(pFile, "The differential correlation for the %d-th experiment is %lf\n", i + 1, log(count / (N * 1.0)) / log(2));
//		}
//
//	}
//	printf("The average correlation of 100 experiments is %lf\n", count_all / 100);
//	fprintf(pFile, "The average correlation of 100 experiments is %lf\n", count_all / 100);
//
//	return 0;
//}
//
//int linear_verify()
//{
//	int i, j, s, t;
//	double count_all = 0;
//	const char *pFileName = "Answer_l.txt";
//	FILE * pFile;
//	fopen_s(&pFile, pFileName, "a");
//
//	unsigned long long mask_in[2] = { 0x40000000, 0x00000000 };
//	unsigned long long mask_out[2] = { 0x80000200, 0x0C080010 };
//
//	printf("#############################################\n");
//	fprintf(pFile, "#############################################\n");
//
//	printf("The number of rounds is %d:\n", Round);
//	fprintf(pFile, "The number of rounds is %d:\n", Round);
//
//	printf("The input mask is:\n");
//	fprintf(pFile, "The input mask is:\n");
//	for (i = 0; i < 2; i++)
//	{
//		printf("0x%08llx ", mask_in[i]);
//		fprintf(pFile, "0x%08llx ", mask_in[i]);
//	}
//	printf("\n");
//	fprintf(pFile, "\n");
//
//	printf("The output mask is:\n");
//	fprintf(pFile, "The output mask is:\n");
//
//	for (i = 0; i < 2; i++)
//	{
//		printf("0x%08llx ", mask_out[i]);
//		fprintf(pFile, "0x%08llx ", mask_out[i]);
//	}
//	printf("\n");
//	fprintf(pFile, "\n");
//
//	for (i = 0; i < 100; i++)
//	{
//		unsigned long long K0 = GenerateRandomValue();
//		unsigned long long K1 = GenerateRandomValue();
//		unsigned long long k[4] = { (K0 >> 32) & 0xffffffff, (K0 >> 0) & 0xffffffff, (K1 >> 32) & 0xffffffff,  (K1 >> 0) & 0xffffffff };
//		unsigned long long * rk = key_schedule(k);
//
//		long long count = 0;
//
//		for (j = 0; j < N; j++)
//		{
//			unsigned long long PT = GenerateRandomValue();
//			unsigned long long pt[2] = { (PT >> 32) & 0xffffffff,  (PT >> 0) & 0xffffffff };
//			
//			unsigned long long * ct = lelbc_enc(pt, rk);
//			unsigned long long CT[2] = { ct[0], ct[1] };
//
//			t = 0;
//
//			for (s = 0; s < 32; s++)
//			{
//				t = t ^ (((mask_in[0] & pt[0]) >> s) & 0x1);
//			}
//			for (s = 0; s < 32; s++)
//			{
//				t = t ^ (((mask_in[1] & pt[1]) >> s) & 0x1);
//			}
//			for (s = 0; s < 32; s++)
//			{
//				t = t ^ (((mask_out[0] & CT[1]) >> s) & 0x1);
//			}
//			for (s = 0; s < 32; s++)
//			{
//				t = t ^ (((mask_out[1] & CT[0]) >> s) & 0x1);
//			}
//			if (t == 0)
//			{
//				count = count + 1;
//			}
//			else
//			{
//				count = count - 1;
//			}
//		}
//
//		count_all += count;
//
//		if (i == 0)
//		{
//			printf("The linear correlation for the %d-st experiment is %lf\n", i + 1, log(abs(count) / (N * 1.0)) / log(2));
//			fprintf(pFile, "The linear correlation for the %d-st experiment is %lf\n", i + 1, log(abs(count) / (N * 1.0)) / log(2));
//		}
//
//		if (i == 1)
//		{
//			printf("The linear correlation for the %d-nd experiment is %lf\n", i + 1, log(abs(count) / (N * 1.0)) / log(2));
//			fprintf(pFile, "The linear correlation for the %d-nd experiment is %lf\n", i + 1, log(abs(count) / (N * 1.0)) / log(2));
//		}
//
//		if (i == 2)
//		{
//			printf("The linear correlation for the %d-rd experiment is %lf\n", i + 1, log(abs(count) / (N * 1.0)) / log(2));
//			fprintf(pFile, "The linear correlation for the %d-rd experiment is %lf\n", i + 1, log(abs(count) / (N * 1.0)) / log(2));
//		}
//
//		if (i >= 3)
//		{
//			printf("The linear correlation for the %d-th experiment is %lf\n", i + 1, log(abs(count) / (N * 1.0)) / log(2));
//			fprintf(pFile, "The linear correlation for the %d-th experiment is %lf\n", i + 1, log(abs(count) / (N * 1.0)) / log(2));
//		}
//
//	}
//
//	printf("The average correlation of 100 experiments is %lf\n", log(abs(count_all / 100) / (N * 1.0)) / log(2));
//	fprintf(pFile, "The average correlation of 100 experiments is %lf\n", log(abs(count_all / 100) / (N * 1.0)) / log(2));
//
//	return 0;
//}

int differential_linear_verify()
{
	int i, j, s, t, r0;
	double cor_min = -100;
	unsigned long long OUTPUT[1][5] = { 0, 0, 0, 0, 0 };
	const char* pFileName = "lelbc_dl_4_4_0.txt";
	FILE* pFile;
	fopen_s(&pFile, pFileName, "a");
	const char* qFileName = "lelbc_dl_4_4_0_clear.txt";
	FILE* qFile;
	fopen_s(&qFile, qFileName, "a");

	unsigned long long IN[245][5] = {{ 0x5000 , 0x0 , 0x0 , 0x80 , 28 },
{ 0x5000 , 0x0 , 0x0 , 0x100 , 28 },
{ 0x5000 , 0x0 , 0x0 , 0x100000 , 28 },
{ 0x5000 , 0x0 , 0x0 , 0x10000000 , 28 },
{ 0x9000 , 0x0 , 0x0 , 0x200 , 28 },
{ 0x9000 , 0x0 , 0x10000 , 0x0 , 28 },
{ 0x9000 , 0x0 , 0x0 , 0x800 , 28 },
{ 0x9000 , 0x0 , 0x8000 , 0x0 , 28 },
{ 0x9000 , 0x0 , 0x0 , 0x400 , 28 },
{ 0x9000 , 0x0 , 0x0 , 0x100 , 28 },
{ 0x9000 , 0x0 , 0x80000 , 0x0 , 28 },
{ 0x9000 , 0x0 , 0x0 , 0x20 , 28 },
{ 0x9000 , 0x0 , 0x0 , 0x100000 , 28 },
{ 0x2000 , 0x0 , 0x10000000 , 0x0 , 28 },
{ 0x2000 , 0x0 , 0x4000000 , 0x0 , 28 },
{ 0x2000 , 0x0 , 0x0 , 0x800000 , 28 },
{ 0x2000 , 0x0 , 0x100000 , 0x0 , 28 },
{ 0x2000 , 0x0 , 0x400000 , 0x0 , 28 },
{ 0x2000 , 0x0 , 0x0 , 0x100000 , 28 },
{ 0x2000 , 0x0 , 0x0 , 0x400000 , 28 },
{ 0x2000 , 0x0 , 0x0 , 0x20000000 , 28 },
{ 0xa000 , 0x0 , 0x40 , 0x0 , 31 },
{ 0xa000 , 0x0 , 0x0 , 0x8 , 31 },
{ 0xa000 , 0x0 , 0x20 , 0x0 , 31 },
{ 0xa000 , 0x0 , 0x10000 , 0x0 , 31 },
{ 0xa000 , 0x0 , 0x0 , 0x40000000 , 31 },
{ 0xa000 , 0x0 , 0x80000 , 0x0 , 31 },
{ 0xa000 , 0x0 , 0x0 , 0x10000 , 31 },
{ 0xa000 , 0x0 , 0x0 , 0x80 , 31 },
{ 0xa000 , 0x0 , 0x400 , 0x0 , 31 },
{ 0xa000 , 0x0 , 0x0 , 0x20000000 , 31 },
{ 0xa000 , 0x0 , 0x800 , 0x0 , 31 },
{ 0xa000 , 0x0 , 0x0 , 0x100 , 31 },
{ 0xa000 , 0x0 , 0x20000000 , 0x0 , 31 },
{ 0xa000 , 0x0 , 0x0 , 0x2000000 , 31 },
{ 0xa000 , 0x0 , 0x0 , 0x8000000 , 31 },
{ 0xa000 , 0x0 , 0x0 , 0x400000 , 31 },
{ 0x4000 , 0x0 , 0x0 , 0x8 , 28 },
{ 0x4000 , 0x0 , 0x0 , 0x4 , 28 },
{ 0x4000 , 0x0 , 0x100 , 0x0 , 28 },
{ 0x4000 , 0x0 , 0x0 , 0x2 , 28 },
{ 0x4000 , 0x0 , 0x200000 , 0x0 , 28 },
{ 0xc000 , 0x0 , 0x0 , 0x800 , 28 },
{ 0xc000 , 0x0 , 0x40 , 0x0 , 28 },
{ 0x8000 , 0x0 , 0x8000000 , 0x0 , 28 },
{ 0x8000 , 0x0 , 0x0 , 0x40000000 , 28 },
{ 0x8000 , 0x0 , 0x0 , 0x20000000 , 28 },
{ 0x8000 , 0x0 , 0x0 , 0x800000 , 28 },
{ 0x10000 , 0x0 , 0x800000 , 0x0 , 28 },
{ 0x10000 , 0x0 , 0x0 , 0x4000000 , 28 },
{ 0x10000 , 0x0 , 0x400000 , 0x0 , 28 },
{ 0x10000 , 0x0 , 0x4000 , 0x0 , 28 },
{ 0x10000 , 0x0 , 0x0 , 0x1000000 , 28 },
{ 0x10000 , 0x0 , 0x0 , 0x8000000 , 28 },
{ 0x10000 , 0x0 , 0x2 , 0x0 , 28 },
{ 0x10000 , 0x0 , 0x2000 , 0x0 , 28 },
{ 0x50000 , 0x0 , 0x0 , 0x8000000 , 28 },
{ 0x50000 , 0x0 , 0x0 , 0x80 , 28 },
{ 0x50000 , 0x0 , 0x10000000 , 0x0 , 28 },
{ 0x50000 , 0x0 , 0x0 , 0x4000 , 28 },
{ 0x90000 , 0x0 , 0x800 , 0x0 , 28 },
{ 0x90000 , 0x0 , 0x400 , 0x0 , 28 },
{ 0x90000 , 0x0 , 0x0 , 0x2000 , 28 },
{ 0x90000 , 0x0 , 0x200 , 0x0 , 28 },
{ 0x90000 , 0x0 , 0x0 , 0x1000 , 28 },
{ 0x90000 , 0x0 , 0x0 , 0x8000 , 28 },
{ 0x20000 , 0x0 , 0x1000 , 0x0 , 28 },
{ 0x20000 , 0x0 , 0x8000 , 0x0 , 28 },
{ 0xa0000 , 0x0 , 0x0 , 0x80 , 31 },
{ 0xa0000 , 0x0 , 0x0 , 0x8000 , 31 },
{ 0xa0000 , 0x0 , 0x0 , 0x20 , 31 },
{ 0xa0000 , 0x0 , 0x0 , 0x1 , 31 },
{ 0xa0000 , 0x0 , 0x0 , 0x40000 , 31 },
{ 0xa0000 , 0x0 , 0x80000000 , 0x0 , 31 },
{ 0xa0000 , 0x0 , 0x0 , 0x200 , 31 },
{ 0xa0000 , 0x0 , 0x400000 , 0x0 , 31 },
{ 0xa0000 , 0x0 , 0x800000 , 0x0 , 31 },
{ 0xa0000 , 0x0 , 0x0 , 0x2000 , 31 },
{ 0x40000 , 0x0 , 0x0 , 0x2000000 , 28 },
{ 0x40000 , 0x0 , 0x0 , 0x4000000 , 28 },
{ 0xc0000 , 0x0 , 0x0 , 0x1 , 28 },
{ 0xc0000 , 0x0 , 0x40000000 , 0x0 , 28 },
{ 0xc0000 , 0x0 , 0x400 , 0x0 , 28 },
{ 0xc0000 , 0x0 , 0x0 , 0x2 , 28 },
{ 0xc0000 , 0x0 , 0x400000 , 0x0 , 28 },
{ 0xc0000 , 0x0 , 0x20000000 , 0x0 , 28 },
{ 0x80000 , 0x0 , 0x100000 , 0x0 , 28 },
{ 0x100000 , 0x0 , 0x20000 , 0x0 , 28 },
{ 0x100000 , 0x0 , 0x40 , 0x0 , 28 },
{ 0x100000 , 0x0 , 0x10 , 0x0 , 28 },
{ 0x100000 , 0x0 , 0x1000000 , 0x0 , 28 },
{ 0x100000 , 0x0 , 0x200000 , 0x0 , 28 },
{ 0x100000 , 0x0 , 0x80 , 0x0 , 28 },
{ 0x100000 , 0x0 , 0x0 , 0x8000000 , 28 },
{ 0x100000 , 0x0 , 0x0 , 0x80 , 28 },
{ 0x100000 , 0x0 , 0x80000000 , 0x0 , 28 },
{ 0x100000 , 0x0 , 0x0 , 0x8000 , 28 },
{ 0x100000 , 0x0 , 0x0 , 0x80000000 , 28 },
{ 0x500000 , 0x0 , 0x0 , 0x80 , 28 },
{ 0x500000 , 0x0 , 0x0 , 0x20000000 , 28 },
{ 0x500000 , 0x0 , 0x10 , 0x0 , 28 },
{ 0x500000 , 0x0 , 0x8 , 0x0 , 28 },
{ 0x500000 , 0x0 , 0x0 , 0x100 , 28 },
{ 0x500000 , 0x0 , 0x80000 , 0x0 , 28 },
{ 0x500000 , 0x0 , 0x0 , 0x80000000 , 28 },
{ 0x500000 , 0x0 , 0x0 , 0x40000 , 28 },
{ 0x900000 , 0x0 , 0x10000 , 0x0 , 28 },
{ 0x900000 , 0x0 , 0x2 , 0x0 , 28 },
{ 0x900000 , 0x0 , 0x8000000 , 0x0 , 28 },
{ 0x900000 , 0x0 , 0x20000 , 0x0 , 28 },
{ 0x900000 , 0x0 , 0x0 , 0x40 , 28 },
{ 0x900000 , 0x0 , 0x0 , 0x8000 , 28 },
{ 0x900000 , 0x0 , 0x40000 , 0x0 , 28 },
{ 0x900000 , 0x0 , 0x40000000 , 0x0 , 28 },
{ 0x900000 , 0x0 , 0x10 , 0x0 , 28 },
{ 0x900000 , 0x0 , 0x1000000 , 0x0 , 28 },
{ 0x900000 , 0x0 , 0x0 , 0x80000 , 28 },
{ 0x900000 , 0x0 , 0x0 , 0x8000000 , 28 },
{ 0x900000 , 0x0 , 0x0 , 0x100000 , 28 },
{ 0x200000 , 0x0 , 0x0 , 0x800000 , 28 },
{ 0x200000 , 0x0 , 0x0 , 0x200000 , 28 },
{ 0xa00000 , 0x0 , 0x2000 , 0x0 , 31 },
{ 0xa00000 , 0x0 , 0x0 , 0x8000 , 31 },
{ 0xa00000 , 0x0 , 0x0 , 0x80000 , 31 },
{ 0xa00000 , 0x0 , 0x10 , 0x0 , 31 },
{ 0x400000 , 0x0 , 0x0 , 0x8 , 28 },
{ 0x400000 , 0x0 , 0x4000000 , 0x0 , 28 },
{ 0x400000 , 0x0 , 0x0 , 0x8000 , 28 },
{ 0x400000 , 0x0 , 0x400000 , 0x0 , 28 },
{ 0x400000 , 0x0 , 0x1 , 0x0 , 28 },
{ 0x400000 , 0x0 , 0x10000000 , 0x0 , 28 },
{ 0x400000 , 0x0 , 0x20 , 0x0 , 28 },
{ 0x400000 , 0x0 , 0x0 , 0x40000 , 28 },
{ 0x400000 , 0x0 , 0x0 , 0x80 , 28 },
{ 0x400000 , 0x0 , 0x200 , 0x0 , 28 },
{ 0x400000 , 0x0 , 0x800 , 0x0 , 28 },
{ 0x400000 , 0x0 , 0x0 , 0x40 , 28 },
{ 0xc00000 , 0x0 , 0x4 , 0x0 , 28 },
{ 0xc00000 , 0x0 , 0x8 , 0x0 , 28 },
{ 0xc00000 , 0x0 , 0x2 , 0x0 , 28 },
{ 0xc00000 , 0x0 , 0x0 , 0x2000000 , 28 },
{ 0xc00000 , 0x0 , 0x0 , 0x40 , 28 },
{ 0xc00000 , 0x0 , 0x0 , 0x20 , 28 },
{ 0x800000 , 0x0 , 0x40 , 0x0 , 28 },
{ 0x800000 , 0x0 , 0x20 , 0x0 , 28 },
{ 0x800000 , 0x0 , 0x80 , 0x0 , 28 },
{ 0x800000 , 0x0 , 0x80000 , 0x0 , 28 },
{ 0x800000 , 0x0 , 0x0 , 0x800000 , 28 },
{ 0x800000 , 0x0 , 0x1000000 , 0x0 , 28 },
{ 0x1000000 , 0x0 , 0x100 , 0x0 , 28 },
{ 0x1000000 , 0x0 , 0x0 , 0x1 , 28 },
{ 0x1000000 , 0x0 , 0x80000000 , 0x0 , 28 },
{ 0x1000000 , 0x0 , 0x40000000 , 0x0 , 28 },
{ 0x5000000 , 0x0 , 0x0 , 0x800 , 28 },
{ 0x5000000 , 0x0 , 0x10 , 0x0 , 28 },
{ 0x5000000 , 0x0 , 0x20 , 0x0 , 28 },
{ 0x9000000 , 0x0 , 0x100 , 0x0 , 28 },
{ 0x9000000 , 0x0 , 0x0 , 0x8000000 , 28 },
{ 0x9000000 , 0x0 , 0x0 , 0x2000000 , 28 },
{ 0x2000000 , 0x0 , 0x0 , 0x80 , 28 },
{ 0x2000000 , 0x0 , 0x1000 , 0x0 , 28 },
{ 0x2000000 , 0x0 , 0x800 , 0x0 , 28 },
{ 0x2000000 , 0x0 , 0x200 , 0x0 , 28 },
{ 0x2000000 , 0x0 , 0x20 , 0x0 , 28 },
{ 0x2000000 , 0x0 , 0x80000 , 0x0 , 28 },
{ 0x2000000 , 0x0 , 0x20000000 , 0x0 , 28 },
{ 0x2000000 , 0x0 , 0x4000 , 0x0 , 28 },
{ 0x2000000 , 0x0 , 0x0 , 0x20 , 28 },
{ 0x2000000 , 0x0 , 0x10000 , 0x0 , 28 },
{ 0x2000000 , 0x0 , 0x80 , 0x0 , 28 },
{ 0x2000000 , 0x0 , 0x0 , 0x400 , 28 },
{ 0x2000000 , 0x0 , 0x0 , 0x200 , 28 },
{ 0x2000000 , 0x0 , 0x400 , 0x0 , 28 },
{ 0xa000000 , 0x0 , 0x0 , 0x100 , 31 },
{ 0xa000000 , 0x0 , 0x0 , 0x400 , 31 },
{ 0x4000000 , 0x0 , 0x100 , 0x0 , 28 },
{ 0x4000000 , 0x0 , 0x0 , 0x8 , 28 },
{ 0x4000000 , 0x0 , 0x2000000 , 0x0 , 28 },
{ 0x4000000 , 0x0 , 0x0 , 0x8000 , 28 },
{ 0x4000000 , 0x0 , 0x0 , 0x4 , 28 },
{ 0x4000000 , 0x0 , 0x40 , 0x0 , 28 },
{ 0x4000000 , 0x0 , 0x400 , 0x0 , 28 },
{ 0x4000000 , 0x0 , 0x0 , 0x20 , 28 },
{ 0x4000000 , 0x0 , 0x0 , 0x80000000 , 28 },
{ 0x4000000 , 0x0 , 0x0 , 0x800 , 28 },
{ 0x4000000 , 0x0 , 0x400000 , 0x0 , 28 },
{ 0x4000000 , 0x0 , 0x10000000 , 0x0 , 28 },
{ 0x4000000 , 0x0 , 0x8000 , 0x0 , 28 },
{ 0xc000000 , 0x0 , 0x0 , 0x80 , 28 },
{ 0x8000000 , 0x0 , 0x0 , 0x80 , 28 },
{ 0x8000000 , 0x0 , 0x20000 , 0x0 , 28 },
{ 0x8000000 , 0x0 , 0x0 , 0x800 , 28 },
{ 0x8000000 , 0x0 , 0x0 , 0x8000000 , 28 },
{ 0x8000000 , 0x0 , 0x2000000 , 0x0 , 28 },
{ 0x8000000 , 0x0 , 0x4000000 , 0x0 , 28 },
{ 0x8000000 , 0x0 , 0x400 , 0x0 , 28 },
{ 0x8000000 , 0x0 , 0x400000 , 0x0 , 28 },
{ 0x8000000 , 0x0 , 0x8000 , 0x0 , 28 },
{ 0x8000000 , 0x0 , 0x100000 , 0x0 , 28 },
{ 0x8000000 , 0x0 , 0x0 , 0x200000 , 28 },
{ 0x8000000 , 0x0 , 0x40000 , 0x0 , 28 },
{ 0x8000000 , 0x0 , 0x20000000 , 0x0 , 28 },
{ 0x8000000 , 0x0 , 0x0 , 0x80000 , 28 },
{ 0x10000000 , 0x0 , 0x4000 , 0x0 , 28 },
{ 0x10000000 , 0x0 , 0x800 , 0x0 , 28 },
{ 0x10000000 , 0x0 , 0x0 , 0x200 , 28 },
{ 0x50000000 , 0x0 , 0x20 , 0x0 , 28 },
{ 0x50000000 , 0x0 , 0x0 , 0x8 , 28 },
{ 0x90000000 , 0x0 , 0x0 , 0x80000 , 28 },
{ 0x90000000 , 0x0 , 0x1000 , 0x0 , 28 },
{ 0x90000000 , 0x0 , 0x1000000 , 0x0 , 28 },
{ 0x90000000 , 0x0 , 0x40000000 , 0x0 , 28 },
{ 0x90000000 , 0x0 , 0x1 , 0x0 , 28 },
{ 0x90000000 , 0x0 , 0x0 , 0x800 , 28 },
{ 0x90000000 , 0x0 , 0x0 , 0x1000000 , 28 },
{ 0x90000000 , 0x0 , 0x800000 , 0x0 , 28 },
{ 0x90000000 , 0x0 , 0x8000000 , 0x0 , 28 },
{ 0x90000000 , 0x0 , 0x0 , 0x40000 , 28 },
{ 0x20000000 , 0x0 , 0x0 , 0x40000 , 28 },
{ 0x20000000 , 0x0 , 0x0 , 0x10000 , 28 },
{ 0x20000000 , 0x0 , 0x0 , 0x20000 , 28 },
{ 0xa0000000 , 0x0 , 0x0 , 0x10000 , 31 },
{ 0xa0000000 , 0x0 , 0x0 , 0x8000000 , 31 },
{ 0xa0000000 , 0x0 , 0x200000 , 0x0 , 31 },
{ 0xa0000000 , 0x0 , 0x400000 , 0x0 , 31 },
{ 0x40000000 , 0x0 , 0x0 , 0x80000 , 28 },
{ 0x40000000 , 0x0 , 0x0 , 0x10000 , 28 },
{ 0x40000000 , 0x0 , 0x0 , 0x20000 , 28 },
{ 0x40000000 , 0x0 , 0x4000000 , 0x0 , 28 },
{ 0x40000000 , 0x0 , 0x0 , 0x40000 , 28 },
{ 0x40000000 , 0x0 , 0x200000 , 0x0 , 28 },
{ 0x40000000 , 0x0 , 0x0 , 0x8 , 28 },
{ 0xc0000000 , 0x0 , 0x0 , 0x4000 , 28 },
{ 0xc0000000 , 0x0 , 0x0 , 0x2 , 28 },
{ 0xc0000000 , 0x0 , 0x0 , 0x2000 , 28 },
{ 0xc0000000 , 0x0 , 0x0 , 0x80 , 28 },
{ 0xc0000000 , 0x0 , 0x2000 , 0x0 , 28 },
{ 0xc0000000 , 0x0 , 0x0 , 0x20000 , 28 },
{ 0x80000000 , 0x0 , 0x10000000 , 0x0 , 28 },
{ 0x80000000 , 0x0 , 0x20000 , 0x0 , 28 },
{ 0x80000000 , 0x0 , 0x80000 , 0x0 , 28 },
{ 0x80000000 , 0x0 , 0x800 , 0x0 , 28 },
{ 0x80000000 , 0x0 , 0x0 , 0x80000 , 28 },
{ 0x80000000 , 0x0 , 0x20000000 , 0x0 , 28 },
{ 0x80000000 , 0x0 , 0x40000 , 0x0 , 28 }};

	for (r0 = 0; r0 < 595; r0++){
		double count_all = 0;
		int count_i = 0;
		printf("#############################################\n");
		printf("r0 = %d < 595 \n", 0 + r0);

		unsigned long long diff_in[2] = { IN[r0][0], IN[r0][1] };
		unsigned long long mask_out[2] = { IN[r0][2], IN[r0][3] };

		printf("#############################################\n");
		fprintf(pFile, "#############################################\n");
		fprintf(qFile, "#############################################\n");

		printf("The number of rounds is %d:\n", Round);
		fprintf(pFile, "The number of rounds is %d:\n", Round);
		fprintf(qFile, "The number of rounds is %d:\n", Round);

		printf("The input difference is:\n");
		fprintf(pFile, "The input difference is:\n");
		fprintf(qFile, "The input difference is:\n");

		for (i = 0; i < 2; i++)
		{
			printf("0x%08llx ", diff_in[i]);
			fprintf(pFile, "0x%08llx ", diff_in[i]);
			fprintf(qFile, "0x%08llx ", diff_in[i]);
		}
		printf("\n");
		fprintf(pFile, "\n");

		printf("The output mask is:\n");
		fprintf(pFile, "The output mask is:\n");
		fprintf(qFile, "The output mask is:\n");

		for (i = 0; i < 2; i++)
		{
			printf("0x%08llx ", mask_out[i]);
			fprintf(pFile, "0x%08llx ", mask_out[i]);
			fprintf(qFile, "0x%08llx ", mask_out[i]);
		}
		printf("\n");
		fprintf(pFile, "\n");

		for (i = 0; i < Times; i++)
		{
			unsigned long long K0 = GenerateRandomValue();
			unsigned long long K1 = GenerateRandomValue();
			unsigned long long k[4] = { (K0 >> 32) & 0xffffffff, (K0 >> 0) & 0xffffffff, (K1 >> 32) & 0xffffffff,  (K1 >> 0) & 0xffffffff };
			unsigned long long rk[32];
			key_schedule(k, rk);
			long long count = 0;


			for (j = 0; j < N; j++)
			{
				unsigned long long PT = GenerateRandomValue();
				unsigned long long pt_0[2] = { (PT >> 32) & 0xffffffff,  (PT >> 0) & 0xffffffff };
				unsigned long long pt_1[2] = { (unsigned long long)(pt_0[0] ^ diff_in[0]), (unsigned long long)(pt_0[1] ^ diff_in[1]) };
				
				unsigned long long ct_0[2];
				lelbc_enc(pt_0, ct_0, rk);
				unsigned long long ct_1[2];
				lelbc_enc(pt_1, ct_1, rk);
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
			//printf("%lld\n", count);

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
				printf("The linear correlation for the %d-st experiment is %lf\n", i + 1, log(abs(count) / (N * 1.0)) / log(2));
				fprintf(pFile, "The linear correlation for the %d-st experiment is %lf\n", i + 1, log(abs(count) / (N * 1.0)) / log(2));
			}

			if (i == 1)
			{
				printf("The linear correlation for the %d-nd experiment is %lf\n", i + 1, log(abs(count) / (N * 1.0)) / log(2));
				fprintf(pFile, "The linear correlation for the %d-nd experiment is %lf\n", i + 1, log(abs(count) / (N * 1.0)) / log(2));
			}

			if (i == 2)
			{
				printf("The linear correlation for the %d-rd experiment is %lf\n", i + 1, log(abs(count) / (N * 1.0)) / log(2));
				fprintf(pFile, "The linear correlation for the %d-rd experiment is %lf\n", i + 1, log(abs(count) / (N * 1.0)) / log(2));
			}

			if (i >= 3)
			{
				printf("The linear correlation for the %d-th experiment is %lf\n", i + 1, log(abs(count) / (N * 1.0)) / log(2));
				fprintf(pFile, "The linear correlation for the %d-th experiment is %lf\n", i + 1, log(abs(count) / (N * 1.0)) / log(2));
			}

		}

		if (count_i == Times)
		{
			printf("The average correlation of 100 experiments is %lf \n", (log(abs(count_all / (Times * 1.0)) / (N * 1.0)) / log(2)));
			fprintf(pFile, "The average correlation of 100 experiments is %lf \n", (log(abs(count_all / (Times * 1.0)) / (N * 1.0)) / log(2)));
			fprintf(qFile, "The average correlation of 100 experiments is %lf \n", (log(abs(count_all / (Times * 1.0)) / (N * 1.0)) / log(2)));
		}
		if ((log(abs(count_all / (Times * 1.0)) / (N * 1.0)) / log(2)) - IN[r0][4] > cor_min) {
			cor_min = (log(abs(count_all / (Times * 1.0)) / (N * 1.0)) / log(2)) - IN[r0][4];
			OUTPUT[0][0] = IN[r0][0];
			OUTPUT[0][1] = IN[r0][1];
			OUTPUT[0][2] = IN[r0][2];
			OUTPUT[0][3] = IN[r0][3];
			OUTPUT[0][4] = IN[r0][4];
		}
	}
	printf("The final input difference  The final output mask \n");
	fprintf(pFile, "The final input difference is: The final output mask is:\n");
	fprintf(qFile, "The final input difference is: The final output mask is:\n");

	printf("[0x%016llx, 0x%016llx], [0x%016llx, 0x%016llx, %lld]\n", OUTPUT[0][0], OUTPUT[0][1], OUTPUT[0][2], OUTPUT[0][3], OUTPUT[0][4]);
	fprintf(pFile, "[0x%016llx, 0x%016llx], [0x%016llx, 0x%016llx, %lld]\n", OUTPUT[0][0], OUTPUT[0][1], OUTPUT[0][2], OUTPUT[0][3], OUTPUT[0][4]);
	fprintf(qFile, "[0x%016llx, 0x%016llx], [0x%016llx, 0x%016llx, %lld]\n", OUTPUT[0][0], OUTPUT[0][1], OUTPUT[0][2], OUTPUT[0][3], OUTPUT[0][4]);

	printf("The final correlation is %lf \n", cor_min);
	fprintf(pFile, "The final correlation is %lf \n", cor_min);
	fprintf(qFile, "The final correlation is %lf \n", cor_min);

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
