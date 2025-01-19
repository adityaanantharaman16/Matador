import Foundation

struct Crypto: Identifiable {
    let id: String                 // Unique identifier (e.g., coin ID like "bitcoin")
    let name: String               // Full name of the cryptocurrency (e.g., Bitcoin)
    let symbol: String             // Symbol of the cryptocurrency (e.g., BTC)
    let description: String?       // Description of the cryptocurrency
    let categories: [String]?      // Categories associated with the cryptocurrency
    let platform: String?          // Platform the crypto operates on (e.g., Ethereum, Binance Smart Chain)
    let currentPriceUSD: Double?   // Current price in USD
    let marketCapUSD: Double?      // Market capitalization in USD
    let volume24h: Double?         // 24-hour trading volume in USD
    let circulatingSupply: Double? // Circulating supply
    let change24h: Double?         // Price change percentage in the last 24 hours

    // Graph information
    let supportedGraphPeriods: [GraphPeriod]   // Supported periods for graphing (e.g., 1d, 1w, 1m)
    let supportedGraphIntervals: [GraphInterval] // Supported intervals for graphing (e.g., 1m, 1h)
}
