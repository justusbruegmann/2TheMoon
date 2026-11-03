import type { CandleChartData, LineChartData } from '../types/chart'

// 5-minute candles for one trading day (2025-01-02, 09:30–16:00 ET = 14:30–21:00 UTC)
export const mockCandleChartData: CandleChartData[] = [
  {
    timestamp: 1735828200000, // 14:30 UTC
    open: 184.95,
    high: 185.2,
    low: 184.87,
    close: 184.98,
  },
  {
    timestamp: 1735828500000, // 14:35 UTC
    open: 184.97,
    high: 185.26,
    low: 184.6,
    close: 184.75,
  },
  {
    timestamp: 1735828800000, // 14:40 UTC
    open: 184.75,
    high: 184.78,
    low: 184.34,
    close: 184.58,
  },
  {
    timestamp: 1735829100000, // 14:45 UTC
    open: 184.62,
    high: 184.69,
    low: 184.52,
    close: 184.59,
  },
  {
    timestamp: 1735829400000, // 14:50 UTC
    open: 184.56,
    high: 184.59,
    low: 184.2,
    close: 184.44,
  },
  {
    timestamp: 1735829700000, // 14:55 UTC
    open: 184.44,
    high: 184.92,
    low: 184.42,
    close: 184.7,
  },
  {
    timestamp: 1735830000000, // 15:00 UTC
    open: 184.7,
    high: 184.96,
    low: 184.29,
    close: 184.43,
  },
  {
    timestamp: 1735830300000, // 15:05 UTC
    open: 184.43,
    high: 184.5,
    low: 184.4,
    close: 184.4,
  },
  {
    timestamp: 1735830600000, // 15:10 UTC
    open: 184.35,
    high: 184.99,
    low: 184.11,
    close: 184.72,
  },
  {
    timestamp: 1735830900000, // 15:15 UTC
    open: 184.73,
    high: 185.13,
    low: 184.63,
    close: 184.94,
  },
  {
    timestamp: 1735831200000, // 15:20 UTC
    open: 184.93,
    high: 185.04,
    low: 184.58,
    close: 184.77,
  },
  {
    timestamp: 1735831500000, // 15:25 UTC
    open: 184.76,
    high: 184.92,
    low: 184.39,
    close: 184.44,
  },
  {
    timestamp: 1735831800000, // 15:30 UTC
    open: 184.44,
    high: 184.5,
    low: 184.3,
    close: 184.32,
  },
  {
    timestamp: 1735832100000, // 15:35 UTC
    open: 184.37,
    high: 184.44,
    low: 184.07,
    close: 184.41,
  },
  {
    timestamp: 1735832400000, // 15:40 UTC
    open: 184.4,
    high: 184.62,
    low: 184.24,
    close: 184.56,
  },
  {
    timestamp: 1735832700000, // 15:45 UTC
    open: 184.61,
    high: 184.82,
    low: 184.27,
    close: 184.39,
  },
  {
    timestamp: 1735833000000, // 15:50 UTC
    open: 184.38,
    high: 184.62,
    low: 184.14,
    close: 184.57,
  },
  {
    timestamp: 1735833300000, // 15:55 UTC
    open: 184.6,
    high: 184.61,
    low: 184.27,
    close: 184.31,
  },
  {
    timestamp: 1735833600000, // 16:00 UTC
    open: 184.32,
    high: 184.39,
    low: 184.09,
    close: 184.24,
  },
  {
    timestamp: 1735833900000, // 16:05 UTC
    open: 184.24,
    high: 184.54,
    low: 183.86,
    close: 183.96,
  },
  {
    timestamp: 1735834200000, // 16:10 UTC
    open: 183.99,
    high: 184.19,
    low: 183.55,
    close: 183.82,
  },
  {
    timestamp: 1735834500000, // 16:15 UTC
    open: 183.82,
    high: 184.1,
    low: 183.64,
    close: 183.78,
  },
  {
    timestamp: 1735834800000, // 16:20 UTC
    open: 183.83,
    high: 184.07,
    low: 183.45,
    close: 183.71,
  },
  {
    timestamp: 1735835100000, // 16:25 UTC
    open: 183.73,
    high: 184.03,
    low: 183.57,
    close: 183.78,
  },
  {
    timestamp: 1735835400000, // 16:30 UTC
    open: 183.76,
    high: 183.85,
    low: 183.52,
    close: 183.65,
  },
  {
    timestamp: 1735835700000, // 16:35 UTC
    open: 183.66,
    high: 183.8,
    low: 183.51,
    close: 183.78,
  },
  {
    timestamp: 1735836000000, // 16:40 UTC
    open: 183.78,
    high: 183.99,
    low: 183.31,
    close: 183.43,
  },
  {
    timestamp: 1735836300000, // 16:45 UTC
    open: 183.42,
    high: 183.79,
    low: 183.29,
    close: 183.75,
  },
  {
    timestamp: 1735836600000, // 16:50 UTC
    open: 183.73,
    high: 183.8,
    low: 183.56,
    close: 183.67,
  },
  {
    timestamp: 1735836900000, // 16:55 UTC
    open: 183.69,
    high: 184.03,
    low: 183.55,
    close: 184.02,
  },
  {
    timestamp: 1735837200000, // 17:00 UTC
    open: 184.05,
    high: 184.12,
    low: 183.93,
    close: 184.08,
  },
  {
    timestamp: 1735837500000, // 17:05 UTC
    open: 184.04,
    high: 184.4,
    low: 184.02,
    close: 184.28,
  },
  {
    timestamp: 1735837800000, // 17:10 UTC
    open: 184.29,
    high: 184.37,
    low: 184.06,
    close: 184.18,
  },
  {
    timestamp: 1735838100000, // 17:15 UTC
    open: 184.16,
    high: 184.31,
    low: 184.07,
    close: 184.25,
  },
  {
    timestamp: 1735838400000, // 17:20 UTC
    open: 184.3,
    high: 184.5,
    low: 183.93,
    close: 184.08,
  },
  {
    timestamp: 1735838700000, // 17:25 UTC
    open: 184.11,
    high: 184.22,
    low: 183.77,
    close: 183.84,
  },
  {
    timestamp: 1735839000000, // 17:30 UTC
    open: 183.82,
    high: 184.11,
    low: 183.36,
    close: 183.58,
  },
  {
    timestamp: 1735839300000, // 17:35 UTC
    open: 183.59,
    high: 183.76,
    low: 183.48,
    close: 183.61,
  },
  {
    timestamp: 1735839600000, // 17:40 UTC
    open: 183.59,
    high: 183.71,
    low: 183.39,
    close: 183.52,
  },
  {
    timestamp: 1735839900000, // 17:45 UTC
    open: 183.5,
    high: 183.53,
    low: 183.18,
    close: 183.4,
  },
  {
    timestamp: 1735840200000, // 17:50 UTC
    open: 183.39,
    high: 183.5,
    low: 182.88,
    close: 183.04,
  },
  {
    timestamp: 1735840500000, // 17:55 UTC
    open: 183.01,
    high: 183.56,
    low: 182.72,
    close: 183.29,
  },
  {
    timestamp: 1735840800000, // 18:00 UTC
    open: 183.32,
    high: 183.47,
    low: 183.07,
    close: 183.13,
  },
  {
    timestamp: 1735841100000, // 18:05 UTC
    open: 183.17,
    high: 183.71,
    low: 183.07,
    close: 183.41,
  },
  {
    timestamp: 1735841400000, // 18:10 UTC
    open: 183.42,
    high: 183.83,
    low: 183.38,
    close: 183.56,
  },
  {
    timestamp: 1735841700000, // 18:15 UTC
    open: 183.58,
    high: 184.24,
    low: 183.54,
    close: 183.95,
  },
  {
    timestamp: 1735842000000, // 18:20 UTC
    open: 183.94,
    high: 184.1,
    low: 183.56,
    close: 183.61,
  },
  {
    timestamp: 1735842300000, // 18:25 UTC
    open: 183.61,
    high: 183.85,
    low: 183.28,
    close: 183.36,
  },
  {
    timestamp: 1735842600000, // 18:30 UTC
    open: 183.33,
    high: 183.55,
    low: 183.1,
    close: 183.22,
  },
  {
    timestamp: 1735842900000, // 18:35 UTC
    open: 183.27,
    high: 183.47,
    low: 183.08,
    close: 183.33,
  },
  {
    timestamp: 1735843200000, // 18:40 UTC
    open: 183.37,
    high: 183.51,
    low: 183.34,
    close: 183.37,
  },
  {
    timestamp: 1735843500000, // 18:45 UTC
    open: 183.4,
    high: 183.57,
    low: 182.97,
    close: 183.15,
  },
  {
    timestamp: 1735843800000, // 18:50 UTC
    open: 183.13,
    high: 183.2,
    low: 182.82,
    close: 183.06,
  },
  {
    timestamp: 1735844100000, // 18:55 UTC
    open: 183.06,
    high: 183.33,
    low: 183.04,
    close: 183.18,
  },
  {
    timestamp: 1735844400000, // 19:00 UTC
    open: 183.19,
    high: 183.38,
    low: 182.95,
    close: 183.33,
  },
  {
    timestamp: 1735844700000, // 19:05 UTC
    open: 183.3,
    high: 183.44,
    low: 182.76,
    close: 182.98,
  },
  {
    timestamp: 1735845000000, // 19:10 UTC
    open: 183.03,
    high: 183.07,
    low: 182.84,
    close: 183.06,
  },
  {
    timestamp: 1735845300000, // 19:15 UTC
    open: 183.05,
    high: 183.17,
    low: 182.94,
    close: 183.06,
  },
  {
    timestamp: 1735845600000, // 19:20 UTC
    open: 183.09,
    high: 183.62,
    low: 182.92,
    close: 183.35,
  },
  {
    timestamp: 1735845900000, // 19:25 UTC
    open: 183.31,
    high: 183.57,
    low: 183.13,
    close: 183.49,
  },
  {
    timestamp: 1735846200000, // 19:30 UTC
    open: 183.44,
    high: 183.63,
    low: 183.16,
    close: 183.42,
  },
  {
    timestamp: 1735846500000, // 19:35 UTC
    open: 183.4,
    high: 183.98,
    low: 183.26,
    close: 183.69,
  },
  {
    timestamp: 1735846800000, // 19:40 UTC
    open: 183.69,
    high: 183.99,
    low: 183.68,
    close: 183.98,
  },
  {
    timestamp: 1735847100000, // 19:45 UTC
    open: 183.98,
    high: 184.14,
    low: 183.82,
    close: 184.02,
  },
  {
    timestamp: 1735847400000, // 19:50 UTC
    open: 184.04,
    high: 184.3,
    low: 184,
    close: 184.11,
  },
  {
    timestamp: 1735847700000, // 19:55 UTC
    open: 184.14,
    high: 184.66,
    low: 184.01,
    close: 184.37,
  },
  {
    timestamp: 1735848000000, // 20:00 UTC
    open: 184.33,
    high: 184.62,
    low: 184,
    close: 184.29,
  },
  {
    timestamp: 1735848300000, // 20:05 UTC
    open: 184.28,
    high: 184.58,
    low: 183.92,
    close: 184.16,
  },
  {
    timestamp: 1735848600000, // 20:10 UTC
    open: 184.15,
    high: 184.17,
    low: 183.74,
    close: 184.02,
  },
  {
    timestamp: 1735848900000, // 20:15 UTC
    open: 184.03,
    high: 184.57,
    low: 183.77,
    close: 184.35,
  },
  {
    timestamp: 1735849200000, // 20:20 UTC
    open: 184.31,
    high: 184.33,
    low: 184.21,
    close: 184.3,
  },
  {
    timestamp: 1735849500000, // 20:25 UTC
    open: 184.28,
    high: 184.5,
    low: 184.01,
    close: 184.23,
  },
  {
    timestamp: 1735849800000, // 20:30 UTC
    open: 184.2,
    high: 184.44,
    low: 183.97,
    close: 184.16,
  },
  {
    timestamp: 1735850100000, // 20:35 UTC
    open: 184.16,
    high: 184.63,
    low: 184.08,
    close: 184.39,
  },
  {
    timestamp: 1735850400000, // 20:40 UTC
    open: 184.36,
    high: 184.55,
    low: 184.25,
    close: 184.48,
  },
  {
    timestamp: 1735850700000, // 20:45 UTC
    open: 184.45,
    high: 184.59,
    low: 184.27,
    close: 184.55,
  },
  {
    timestamp: 1735851000000, // 20:50 UTC
    open: 184.54,
    high: 184.7,
    low: 184.15,
    close: 184.27,
  },
  {
    timestamp: 1735851300000, // 20:55 UTC
    open: 184.26,
    high: 184.6,
    low: 184.23,
    close: 184.59,
  },
]

export const mockLineChartData: LineChartData[] = mockCandleChartData.map(c => ({
  timestamp: c.timestamp,
  value: +((c.open + c.high + c.low + c.close) / 4).toFixed(2),
}))
