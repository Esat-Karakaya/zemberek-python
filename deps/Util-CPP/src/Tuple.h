//
// Created by Olcay Taner Yıldız on 29.09.2018.
//

#ifndef UTIL_TUPLE_H
#define UTIL_TUPLE_H


class Tuple {
private:
    int first;
    int last;
public:
    Tuple(int first, int last);
    [[nodiscard]] int getFirst() const;
    [[nodiscard]] int getLast() const;
};


#endif //UTIL_TUPLE_H
