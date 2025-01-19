import Foundation

struct Stock: Identifiable {
    let id: String                 // Unique identifier (symbol/ticker)
    let name: String               // Full company name
    let symbol: String             // Stock ticker symbol (e.g., AAPL)
    let sector: String?            // Sector the company operates in (e.g., Technology)
    let industry: String?          // Industry the company belongs to (e.g., Consumer Electronics)
    let price: Double?             // Current stock price
    let marketCap: Double?         // Market capitalization
    let peRatio: Double?           // Price-to-earnings ratio
    let volume: Int?               // Current trading volume
    let fiftyTwoWeekHigh: Double?  // 52-week high price
    let fiftyTwoWeekLow: Double?   // 52-week low price

    // Graph information
    //let supportedGraphPeriods: [GraphPeriod] // Time periods supported for graphing (e.g., 1d, 5d, 1mo)
    //let supportedGraphIntervals: [GraphInterval] // Intervals supported for each graph period (e.g., 1m, 5m)
}

// Enum for graph periods (e.g., 1 day, 5 days, 1 month)
enum GraphPeriod: String {
    case oneDay = "1d"
    case fiveDays = "5d"
    case oneMonth = "1mo"
    case sixMonths = "6mo"
    case oneYear = "1y"
}

// Enum for graph intervals (e.g., 1 minute, 1 hour, 1 day)
enum GraphInterval: String {
    case oneMinute = "1m"
    case fiveMinutes = "5m"
    case oneHour = "1h"
    case oneDay = "1d"
}
