import SwiftUI

// Mock User
let mockUser = User(
    id: UUID(),
    username: "@sarahc",
    name: "Sarah Chen",
    profilePicture: "https://via.placeholder.com/150", // Placeholder image URL
    bio: "Investor in stocks and crypto.",
    followers: [],
    following: [],
    stockKarma: 1200,
    totalStockLikes: 500,
    totalStockPitches: 30,
    cryptoKarma: 800,
    totalCryptoLikes: 300,
    totalCryptoPitches: 15,
    stockPitches: [],
    likedStockPitches: [],
    cryptoPitches: [],
    likedCryptoPitches: []
)

// Mock Stock
let mockStock = Stock(
    id: "AAPL", // Apple Inc. ticker symbol
    name: "Apple Inc.",
    symbol: "AAPL",
    sector: "Technology",
    industry: "Consumer Electronics",
    price: 180.95,
    marketCap: 2.8e12,
    peRatio: 29.5,
    volume: 50_000_000,
    fiftyTwoWeekHigh: 190.00,
    fiftyTwoWeekLow: 120.00
)

// Mock Comments
let mockComments = [
    Comment(
        id: UUID(),
        user: mockUser,
        content: "Great pitch! I totally agree.",
        createdAt: Date(),
        likes: 10,
        parentCommentID: nil,
        replies: []
    )
]

// Mock StockPitch
let mockStockPitch = StockPitch(
    id: UUID(),
    user: mockUser,
    stock: mockStock,
    thesis: "Apple's services segment is growing rapidly, making it a great investment opportunity for the long term.",
    pitchPrice: 175.0,
    returnPercentage: 3.4,
    likes: 245,
    comments: mockComments,
    shares: 18,
    createdAt: Date()
)

// ForYouPage View
struct ForYouPage: View {
    var stockPitches: [StockPitch] = [mockStockPitch] // Replace with actual data source

    var body: some View {
        NavigationView {
            ScrollView {
                VStack(spacing: 20) {
                    ForEach(stockPitches) { pitch in
                        NavigationLink(destination: FullyOpenedPitchView(stockPitch: pitch)) {
                            FullyOpenedPitchView(stockPitch: pitch) // Assume a compact view exists
                        }
                    }
                }
                .padding()
            }
            .navigationTitle("For You")
        }
    }
}
