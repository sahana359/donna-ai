//
//  ThinkingBubble.swift
//  ui
//
//  Created by Sahana Rajashekara on 2/9/26.
//

import SwiftUI

struct ThinkingBubble: View {
    @State private var dotCount: Int = 0
    
    var body: some View {
        HStack {
            HStack(spacing: 4) {
                Text("Thinking")
                    .foregroundColor(.gray)
                
                Text(String(repeating: ".", count: dotCount))
                    .foregroundColor(.gray)
                    .frame(width: 20, alignment: .leading)
            }
            .padding(12)
            .background(Color.gray.opacity(0.2))
            .cornerRadius(16)
            
            Spacer()
        }
        .onAppear {
            startAnimation()
        }
    }
    
    private func startAnimation() {
        Timer.scheduledTimer(withTimeInterval: 0.4, repeats: true) { timer in
            dotCount = (dotCount % 3) + 1
        }
    }
}

#Preview {
    ThinkingBubble()
        .padding()
}
