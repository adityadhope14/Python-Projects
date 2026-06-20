#include <iostream>
#include <vector>
#include <map>
using namespace std;
void solving() {
    int n;
    cin >> n;
    map<int, int> counts;
    for (int i = 0; i < n; i++) {
        int num;
        cin >> num;
        counts[num]++; 
    }
    if (counts.size() > 2) {
        cout << "No\n";
    } 
    else if (counts.size() == 1) {
        cout << "Yes\n";
    } 
    else {
        int freq1 = counts.begin()->second;
        if (freq1 == n / 2 || freq1 == (n + 1) / 2) {
            cout << "Yes\n";
        } else {
            cout << "No\n";
        }
    }
}
int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    int t;
    cin >> t;
    while (t--) {
        solving();
    }
    return 0;
}