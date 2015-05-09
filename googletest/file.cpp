%{Cpp:LicenseTemplate}\
#include "gtest/gtest.h"

/**
 * @brief Automatically generated Google Test skeleton
 */
class %{TestName} : public ::testing::Test
{
protected:
    %{TestName}() {
        // You can do set-up work for each test here.
    }

    virtual ~%{TestName}() {
        // You can do clean-up work that doesn't throw exceptions here.
    }

    void SetUp() {
        // Code here will be called immediately after the constructor (right
        // before each test).
    }

    void TearDown() {
        // Code here will be called immediately after each test (right
        // before the destructor).
    }

    static void SetUpTestCase() {
        // Called before the first test in this test case.
    }

    static void TearDownTestCase() {
        // Called after the last test in this test case.
    }
};

TEST_F(%{TestName}, FirstTest) {
    // Test
}
