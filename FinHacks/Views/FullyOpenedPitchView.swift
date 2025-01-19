import SwiftUI

struct FullyOpenedPitchView: View {
    let stockPitch: StockPitch

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 20) {
                // Header Section
                HStack {
                    AsyncImage(url: URL(string: stockPitch.user.profilePicture)) { image in
                        image.resizable()
                    } placeholder: {
                        Color.gray.opacity(0.3)
                    }
                    .frame(width: 50, height: 50)
                    .clipShape(Circle())

                    VStack(alignment: .leading) {\
                        Text(stockPitch.user.name)
                            .font(.headline)
                        Text(stockPitch.user.username)
                            .font(.subheadline)
                            .foregroundColor(.gray)
                    }

                    Spacer()
                    Button(action: {
                        // Follow/Unfollow action
                    }) {
                        Text("Follow")
                            .font(.subheadline)
                            .padding(.horizontal, 10)
                            .padding(.vertical, 5)
                            .background(Color.blue)
                            .foregroundColor(.white)
                            .cornerRadius(8)
                    }
                }

                // Stock Information
                VStack(alignment: .leading, spacing: 10) {
                    HStack {
                        Text(stockPitch.stock.symbol)
                            .font(.title)
                            .bold()
                        Text("$\(stockPitch.stock.price ?? 0, specifier: "%.2f")")
                            .foregroundColor(.gray)
                        Text("\(stockPitch.returnPercentage > 0 ? "+" : "")\(stockPitch.returnPercentage, specifier: "%.2f")%")
                            .foregroundColor(stockPitch.returnPercentage > 0 ? .green : .red)
                            .fontWeight(.bold)
                    }

                    Text(stockPitch.stock.name)
                        .font(.subheadline)
                        .foregroundColor(.gray)

                    HStack {
                        Text("Market Cap: \(formatMarketCap(stockPitch.stock.marketCap ?? 0))")
                            .font(.footnote)
                            .foregroundColor(.gray)
                        Spacer()
                        Text("Sector: \(stockPitch.stock.sector ?? "N/A")")
                            .font(.footnote)
                            .foregroundColor(.gray)
                    }
                }

                // Pitch Content
                Text(stockPitch.thesis)
                    .font(.body)
                    .foregroundColor(.black)
                    .padding(.vertical)

                // Graph/Visualization Placeholder
                VStack {
                    Text("Stock Price History")
                        .font(.headline)
                    Rectangle()
                        .fill(Color.gray.opacity(0.2))
                        .frame(height: 200)
                        .cornerRadius(10)
                        .overlay(Text("Graph Placeholder").foregroundColor(.gray))
                }

                // Interaction Section
                HStack {
                    HStack(spacing: 5) {
                        Image(systemName: "hand.thumbsup")
                        Text("\(stockPitch.likes)")
                    }

                    HStack(spacing: 5) {
                        Image(systemName: "message")
                        Text("\(stockPitch.comments.count)")
                    }

                    HStack(spacing: 5) {
                        Image(systemName: "arrowshape.turn.up.right")
                        Text("\(stockPitch.shares)")
                    }
                }
                .font(.footnote)
                .foregroundColor(.gray)

                Divider()

                // Comments Section
                Text("Comments")
                    .font(.headline)

                if stockPitch.comments.isEmpty {
                    Text("No comments yet. Be the first to comment!")
                        .font(.subheadline)
                        .foregroundColor(.gray)
                } else {
                    ForEach(stockPitch.comments) { comment in
                        CommentView(comment: comment)
                    }
                }

                // Add Comment Section
                HStack {
                    TextField("Write a comment...", text: .constant(""))
                        .textFieldStyle(RoundedBorderTextFieldStyle())

                    Button(action: {
                        // Add comment action
                    }) {
                        Image(systemName: "paperplane.fill")
                            .foregroundColor(.blue)
                            .padding()
                    }
                }
            }
            .padding()
        }
        .navigationTitle("Pitch")
        .navigationBarTitleDisplayMode(.inline)
    }

    private func formatMarketCap(_ marketCap: Double) -> String {
        if marketCap >= 1e12 {
            return String(format: "%.1fT", marketCap / 1e12)
        } else if marketCap >= 1e9 {
            return String(format: "%.1fB", marketCap / 1e9)
        } else {
            return String(format: "%.1fM", marketCap / 1e6)
        }
    }
}
