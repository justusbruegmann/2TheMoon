import type { Holding } from '../types/holding'

// assetIds reference real assets returned by GET /assets/
export const mockHoldings: Holding[] = [
  { assetId: '1cd93b2b-48b7-48e3-b496-9afb9cffd2aa', quantity: 8, avgBuyPrice: 245.3 }, // TSLA
  { assetId: 'fe5a4091-c01d-40cd-847c-e5765e4304f9', quantity: 3, avgBuyPrice: 1420.0 }, // RHM
  { assetId: 'cf827f02-60c2-4390-a9a4-9326afb98d18', quantity: 20, avgBuyPrice: 138.6 }, // AMD
  { assetId: 'dd00c57d-e82a-41a2-8eeb-1815e1686c6d', quantity: 25, avgBuyPrice: 172.4 }, // APC (Apple)
  { assetId: 'fb542482-5b97-4dd6-a235-c1e02a20d467', quantity: 40, avgBuyPrice: 98.7 }, // NVD (NVIDIA)
  { assetId: 'bdd640fb-0667-4ad1-9c80-317fa3b1799d', quantity: 10, avgBuyPrice: 185.2 }, // SAP
  { assetId: '23b8c1e9-3924-46de-beb1-3b9046685257', quantity: 6, avgBuyPrice: 268.5 }, // ALV (Allianz)
  { assetId: 'bd9c66b3-ad3c-4d6d-9a3d-1fa7bc8960a9', quantity: 12, avgBuyPrice: 89.4 }, // BMW
]
