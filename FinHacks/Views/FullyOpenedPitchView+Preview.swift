import SwiftUI

struct FullyOpenedPitchView_Previews: PreviewProvider {
    static var previews: some View {
        let mockUser = User(
            id: UUID(),
            username: "@sarahc",
            name: "Sarah Chen",
            profilePicture: "https://via.placeholder.com/150",
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

        let mockStock = Stock(
            id: "AAPL",
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

        let mockPitch = StockPitch(
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

        return FullyOpenedPitchView(stockPitch: mockPitch)
    }
}
