// @ts-ignore

export type AssetKind = 'Stock' | 'Crypto' | 'CustomCrypto'

export type Industry =
  | 'Technology'
  | 'Finance'
  | 'Healthcare'
  | 'Energy'
  | 'Consumer'
  | 'Industrials'
  | 'Utilities'
  | 'RealEstate'
  | 'Telecommunications'
  | 'Materials'
  | 'Blockchain'
  | 'Meme'

export type Asset = {
  id: string
  ticker: string
  name: string
  kind: AssetKind
  industry: Industry[]
  creator_id: string | null
  created_at: string
}
