import SwiftUI

struct CommentView: View {
    let comment: Comment

    var body: some View {
        HStack(alignment: .top, spacing: 10) {
            AsyncImage(url: URL(string: comment.user.profilePicture)) { image in
                image.resizable()
            } placeholder: {
                Color.gray.opacity(0.3)
            }
            .frame(width: 40, height: 40)
            .clipShape(Circle())

            VStack(alignment: .leading) {
                Text(comment.user.name)
                    .font(.headline)
                Text(comment.content)
                    .font(.body)
                    .foregroundColor(.black)
                Text("\(comment.createdAt, formatter: dateFormatter)")
                    .font(.footnote)
                    .foregroundColor(.gray)
            }

            Spacer()
            HStack {
                Image(systemName: "hand.thumbsup")
                Text("\(comment.likes)")
            }
            .font(.footnote)
            .foregroundColor(.gray)
        }
        .padding(.vertical, 5)
    }

    private var dateFormatter: DateFormatter {
        let formatter = DateFormatter()
        formatter.dateStyle = .short
        formatter.timeStyle = .short
        return formatter
    }
}
