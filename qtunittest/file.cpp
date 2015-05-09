%{Cpp:LicenseTemplate}\
#include <QtTest>

/**
 * @brief Automatically generated Qt Unit Test skeleton
 */
class %{TestName} : public QObject
{
    Q_OBJECT
public:
    %{TestName}(){}

private slots:
    void initTestCase(){}
    void cleanupTestCase(){}
    void init(){}
    void cleanup(){}
    
    void firstTest();
};

void %{TestName}::firstTest()
{
}

QTEST_APPLESS_MAIN(%{TestName})
#include "%{JS: Cpp.classToFileName('tst_%{TestName}', 'moc')}"
